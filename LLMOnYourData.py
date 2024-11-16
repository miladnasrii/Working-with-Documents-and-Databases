import sqlite3
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

nlp_model = pipeline("text2text-generation", model="cssupport/t5-small-awesome-text-to-sql")

tokenizer = AutoTokenizer.from_pretrained("cssupport/t5-small-awesome-text-to-sql")
model = AutoModelForSeq2SeqLM.from_pretrained("cssupport/t5-small-awesome-text-to-sql")

def execute_query(query):
    db_path = "/content/drive/MyDrive/Databases/students (1).db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except Exception as e:
        return f"Error executing the query: {e}"
    finally:
        conn.close()

def natural_language_to_sql(question):
    input_text = f"Translate the following natural language query into SQL: {question}"
    output = nlp_model(input_text, max_length=256, truncation=True)
    sql_query = output[0]["generated_text"]

    if not sql_query.strip().lower().startswith(("select", "insert", "update", "delete")):
        raise ValueError("The generated query is not valid: " + sql_query)
    return sql_query

def format_response(query_results):
    if not query_results:
        return "Sorry, no information found!"
    if isinstance(query_results, str):
        return query_results
    response = "Output:\n"
    for row in query_results:
        response += " | ".join(map(str, row)) + "\n"
    return response

def chatbot():
    print("Hi! Please ask your question. (Type 'exit' for quiet chatbot).")
    while True:
        user_input = input("\n> Your question: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        try:
            sql_query = natural_language_to_sql(user_input)
            print(f"\n[Query Generated]: {sql_query}")

            results = execute_query(sql_query)

            response = format_response(results)
            print(response)
        except Exception as e:
            print(f"An error occurred: {str(e)}")

chatbot()

