AGENTS_DIR = COMPETITION_SRC / "agents"

def _load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    mod.__package__ = name.rsplit(".", 1)[0]
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

_load_module("agents.recorder", AGENTS_DIR / "recorder.py")
_load_module("agents.tracing", AGENTS_DIR / "tracing.py")
Agent = _load_module("agents.agent", AGENTS_DIR / "agent.py").Agent

_agents_pkg = types.ModuleType("agents")
_agents_pkg.__path__ = [str(AGENTS_DIR)]
_agents_pkg.__package__ = "agents"
_agents_pkg.AVAILABLE_AGENTS = {}
sys.modules["agents"] = _agents_pkg

SIMPLE_ACTIONS = [a for a in GameAction if a.is_simple() and a is not GameAction.RESET]
ALL_ACTIONS = [a for a in GameAction if a is not GameAction.RESET]

class PatternMemory:
    def __init__(self, max_size=5000):
        self.transitions = defaultdict(lambda: defaultdict(int))
        self.state_visits = defaultdict(int)
        self.action_success = defaultdict(lambda: [0, 0])
        self.max_size = max_size
    def record(self, state_key, action_val, won):
        self.transitions[state_key][action_val] += 1
        self.state_visits[state_key] += 1
        self.action_success[action_val][0] += 1 if won else 0
        self.action_success[action_val][1] += 1
        if len(self.transitions) > self.max_size:
            del self.transitions[next(iter(self.transitions))]
    def success_rate(self, action_val):
        s = self.action_success[action_val]
        return s[0] / max(s[1], 1)
    def best_action_from(self, state_key):
        if state_key not in self.transitions:
            return None
        return max(self.transitions[state_key], key=self.transitions[state_key].get)

_global_memory = PatternMemory()

class LLMAgent(Agent):
    MAX_ACTIONS = 360
    SEED = 1850
    DEAD_ZONES = (0,) * 10
    LLM_CALLS = 0
    LLM_ERRORS = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._rng = random.Random(self.SEED + hash(self.game_id) % 10000)
        self.visited = set()
        self.action_count = 0
        self.prev_state_key = None
        self.last_levels = 0
        self.stuck_count = 0
        self.last_action_val = None
        self.consecutive_same = 0
        self.memory = _global_memory

    @property
    def name(self):
        return f"{super().name}.llm.v10"

    def is_done(self, frames, latest_frame):
        return latest_frame.state is GameState.WIN

    def _query_llm(self, frame_text, state_desc):
        if not LLM_AVAILABLE or llm is None:
            return None
        if LLMAgent.LLM_CALLS > 300:
            return None
        action_names = ", ".join(a.name for a in ALL_ACTIONS)
        prompt = (
            f"ARC-AGI-3 game. Choose BEST action.\n"
            f"State: {state_desc}\n"
            f"Frame:\n{frame_text}\n\n"
            f"Actions: {action_names}\n"
            f"Reply ONLY the action name, e.g. ACTION1."
        )
        try:
            LLMAgent.LLM_CALLS += 1
            resp = llm.create_chat_completion(
                messages=[{"role": "user", "content": prompt}],
                max_tokens=20,
                temperature=0.1,
            )
            text = resp["choices"][0]["message"]["content"].strip().upper()
            for a in ALL_ACTIONS:
                if a.name in text:
                    return a
            return None
        except Exception:
            LLMAgent.LLM_ERRORS += 1
            return None

    def _heuristic_decide(self, physics, state_key):
        best = self.memory.best_action_from(state_key)
        if best is not None:
            for a in ALL_ACTIONS:
                if a.value == best:
                    return a
        trits = ternarize(physics, self.DEAD_ZONES)
        v_t = trits[8] if len(trits) > 8 else Trit.ZERO
        r_t = trits[2] if len(trits) > 2 else Trit.ZERO
        g_t = trits[0] if len(trits) > 0 else Trit.ZERO
        if v_t == Trit.POS:
            return GameAction.ACTION1
        elif v_t == Trit.NEG:
            return GameAction.ACTION2
        elif r_t == Trit.POS:
            return GameAction.ACTION3
        elif g_t == Trit.NEG:
            return GameAction.ACTION4
        return self._rng.choice(SIMPLE_ACTIONS)

    def choose_action(self, frames, latest_frame):
        if latest_frame.state in [GameState.NOT_PLAYED, GameState.GAME_OVER]:
            self.visited.clear()
            self.action_count = 0
            self.stuck_count = 0
            self.consecutive_same = 0
            return GameAction.RESET

        physics = extract_physics(latest_frame.frame)
        state_key = physics.key()

        levels = latest_frame.levels_completed if hasattr(latest_frame, "levels_completed") else 0
        if levels > self.last_levels:
            self.stuck_count = 0
        else:
            self.stuck_count += 1
        self.last_levels = levels

        action = None
        if self.stuck_count > 8 and LLM_AVAILABLE:
            frame_text = frame_to_ascii(latest_frame.frame)
            state_desc = (
                f"G={physics.G} D={physics.D} R={physics.R} A={physics.A} "
                f"I={physics.I} N={physics.N} U={physics.U} C={physics.C} "
                f"V={physics.V} T={physics.T} levels={levels} count={self.action_count}"
            )
            action = self._query_llm(frame_text, state_desc)

        if action is None:
            action = self._heuristic_decide(physics, state_key)

        if action.value == self.last_action_val:
            self.consecutive_same += 1
        else:
            self.consecutive_same = 0
        self.last_action_val = action.value

        if self.consecutive_same >= 5:
            alts = [a for a in SIMPLE_ACTIONS if a.value != action.value]
            action = self._rng.choice(alts)
            self.consecutive_same = 0

        won = latest_frame.state is GameState.WIN
        self.memory.record(self.prev_state_key or state_key, action.value, won)
        self.prev_state_key = state_key
        self.visited.add(state_key)
        self.action_count += 1

        if action.is_simple():
            action.reasoning = f"{action.name} phys({physics.as_tuple()})"
        elif action.is_complex():
            action.set_data({"x": 32, "y": 32})
            action.reasoning = f"complex({action.name})"

        return action

print(f"LLMAgent v10 defined (LLM={LLM_AVAILABLE})")
