from src.generator import ChatGenerator, chat_main

# generator = ChatGenerator()
# chain = generator.main()
while True:
    try:
        user_input = input("\nEnter your question (or 'quit' to exit): ")
        
        if user_input.lower() == 'quit':
            print("Goodbye!")
            break
            
        response = chat_main(user_input)
        print("\nResponse:", response)
        
    except KeyboardInterrupt:
        print("\nGoodbye!")
        break
    except Exception as e:
        print(f"\nError: {e}")