fund_manager = {
  "prompt": """Who or what are the fund managers mentioned in the document?" Return the name of fund managers in the context provided as comma separated strings: 'entity1', 'entity2'. 
  If you can't find any fund managers in the context provided, return an empty string. Don't return anything else as the response. Fund managers invest in funds, securities or companies. 
  The fund manager name is often implied near the name of the entities it invests in. The manager name is present across multiple sections. Fund managers hold assets worth a dollar value."""
}

investments = {
  "prompt": """Who or what are the investments mentioned in the document? Return the name of investments in the context provided as comma separated strings: 'entity1', 'entity2'. 
  If you can't find any investments in the context provided, return an empty string. Don't return anything else as the response.
  Investments are organizations, subsidiaries, assets, companies, or otherwise described as words, phrases, acronyms (two letter or three letter: FF, FFA), that are invested in by funds or fund managers. Decisions often end with an investment.""",
}

ic_mrc_arc_prompts = {
  "fund_managers": fund_manager,
  "investments": investments,
}