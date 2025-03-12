document_name = {
  "prompt": "What is the document name?",
  "response_format": "Only return the name of the document in this format: '<name>'. If the document name is not mentioned, return an empty string: "". Don't return anything else as the response. Return only one document name, else return all in a comma-separated strings: '<name1>', '<name2>'",
  "response_type": "static",
  "helper_text": "Usually the document name is the page title or page header of the page 1.",
}

reporting_entity = {
  "prompt": "What is the reporting entity in the document?",
  "response_format": "Only return the name of the reporting entity in this format: '<company name>'. If the reporting entity is not mentioned, return an empty string: "". Don't return anything else as the response. Return only one reporting entity, else return all in a comma-separated strings: '<entity1>', '<entity2>'.",
  "response_type": "static",
  "helper_text": "Usually the reporting entity is the name of the company that prepared the document.",
}

included_entities = {
  "prompt": "What are the included entities in the document?",
  "response_format": "Return the name of entities in the context provided in comma-separated strings: '<entity1>', '<entity2>']. If you can't find any entities in the context provided, return an empty string in a list: "". Don't return anything else as the response.",
  "response_type": "static",
  "helper_text": "The included entities are the organizations, subsidiaries, or entities explicitly listed as part of the reporting or operations scope in the document.",
}

company_identifiers = {
  "prompt": "What are the company identifiers in the document?",
  "response_format": "Only return the identifiers in comma-separated strings: 'ABN <identifier1>', 'ACN <identifier2>'. If no identifiers are mentioned, return an empty string in a list: ""]. Don't return anything else as the response.",
  "response_type": "static",
  "helper_text": "Company identifiers include ABN, ACN, CAN, or similar registration numbers explicitly mentioned in the document.",
}

# registered_addresses = {
#   "prompt": "What are the addresses explicitly mentioned in the document, including both physical addresses and GPO Box addresses? Don't include addresses that are not explicitly mentioned in the document.",
#   "response_format": "Only return the addresses in a comma-separated list: [<address1>,<address2>]. If no addresses are mentioned, return an empty string in a list: [""]. Don't return anything else as the response.",
#   "response_type": "static",
#   "helper_text": "Physical addresses are physical locations such as registered offices or headquarters explicitly stated in the document. GPO Box addresses are mailing addresses starting with 'GPO Box'.",
# }

# phone_numbers = {
#   "prompt": "What are the phone numbers mentioned in the document? A valid phone number should contain only numbers, brackets, spaces, and plus signs.",
#   "response_format": "Only return the phone numbers in comma-separated list: [<phone_number1>, <phone_number2>]. If no phone numbers are mentioned, return an empty string in a list: [""]. Don't return anything else as the response.",
#   "response_type": "static",
#   "helper_text": "Your response should only contain numbers, brackets, spaces, and plus signs.",
# }

# people_roles = {
#   "prompt": "What are the names of individuals and their job title explicitly mentioned in the document? Only respond with their name and job title. Don't respond with anything else.",
#   "response_format": "Only return the people and their job titles in a comma separated list: [<person1 - job_title1>, <person2 - job_title2>]. If no people and their job titles are mentioned, return an empty string in a list: [""]. Don't return anything else as the response.",
#   "response_type": "static",
#   "helper_text": "",
# }

# reporting_period = {
#   "prompt": "Identify the date or reporting period or date range or financial year mentioned in the document (e.g. 31 December 2023, FY 2023, 01 January to 31 December 2023) applicable to the contents of this document.",
#   "response_format": "If you found a reporting date, give your answer in this format: <date> and if you found a date period, give your answer in this format: From <start_date> to <end_date>. If you find a financial year, give your answer in this format: <financial_year>. If you can't find any of the above, you can give the document signed date at the end of the document in this format: '<date>'. If you can't find any dates or periods at all, return an empty string: [""]. Don't return anything else as the response. Return only one date, else return more than one in a comma-separated list.",
#   "response_type": "static",
#   "helper_text": "",
# }

# geographies = {
#   "prompt": "Identify the geographies mentioned in the document (e.g. Australia, UK, USA).",
#   "response_format": "Only return the geographies in comma-separated list: [<geography1>, <geography2>]. If no geographies are mentioned, return an empty string in a list: [""]. Don't return anything else as the response.",
#   "response_type": "static",
#   "helper_text": "",
# }

# currencies = {
#   "prompt": "Identify the currencies mentioned in the document (e.g. AUD, USD, EUR).",
#   "response_format": "Only return the currencies in comma-separated list: [<currency1>, <currency2>]. If no currencies are mentioned, return an empty string in a list: [""]. Don't return anything else as the response.",
#   "response_type": "static",
#   "helper_text": "",
# }

foundational_prompts = {
  "document_name": document_name,
  "reporting_entity": reporting_entity,
  "included_entities": included_entities,
  "company_identifiers": company_identifiers,
#   "registered_addresses": registered_addresses,
#   "phone_numbers": phone_numbers,
#   "people_roles": people_roles,
#   "reporting_period": reporting_period,
#   "geographies": geographies,
#   "currencies": currencies,
}