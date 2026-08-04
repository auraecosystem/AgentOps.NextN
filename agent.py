if games:
    swarm = Swarm(
        agent="llmagent",
        ROOT_URL=ROOT_URL,
        games=games,
        tags=["llm", "qwen3", "v13"],
    )
    swarm.main()
    print(f"Swarm done. LLM calls: {LLMAgent.LLM_CALLS}, errors: {LLMAgent.LLM_ERRORS}")
else:
    print("No games available")

sub_path = WORKING_DIR / "submission.parquet"
if sub_path.exists():
    import pandas as pd
    df = pd.read_parquet(sub_path)
    print(f"Submission: {len(df)} rows, columns={list(df.columns)}")
else:
    print("No submission.parquet found")
