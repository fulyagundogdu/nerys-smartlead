from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(port=5000, debug=True)


from openai import OpenAI

client = OpenAI()

response = client.completions.create(
    model="gpt-3.5-turbo-instruct", prompt="Write a tagline for an parfum shop."
)