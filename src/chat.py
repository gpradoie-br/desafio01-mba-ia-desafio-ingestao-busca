from search import search_prompt

def main():
    print("Faça sua pergunta (digite 'sair' para encerrar):")

    while True:
        question = input("\nPERGUNTA: ").strip()

        if question.lower() in ("sair", "exit", "quit"):
            break

        resposta = search_prompt(question)
        print(f"RESPOSTA: {resposta}")


if __name__ == "__main__":
    main()