MODEL_LIST:list[str] = ["gemini-2.5-flash","gemini-2.5-flash-lite"]
DEPARTMENTS = ['INFO','PAYMENT','MANAGEMENT']
retry_config:dict = {
    "attempts":3,
    "initial_delay":1,
    "exp_base":2
}
