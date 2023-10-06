import streamlit as st
from simpleai.search import CspProblem, backtrack
import pandas as pd

# Function to check if a solution is valid
def is_valid_solution(variables, values):
    # Ensure that each variable has a unique and different value
    if len(values) != len(set(values)):
        return False
    
    # Make sure numbers don't start with zero
    for word in words:
        if values[variables.index(word[0])] == 0:
            return False
    
    # Replace letters with values and check the correctness of the arithmetic operation
    exp = puzzle_input
    for i, letter in enumerate(variables):
        exp = exp.replace(letter, str(values[i]))
    
    try:
        return eval(exp) == 0  # Here, we evaluate the expression and check if it equals zero
    except ZeroDivisionError:
        return False

# Function to solve the cryptarithmetic puzzle
def cryptarithmetic_solver(words):

    # Create a list of unique letters from the words
    letters = list(set(''.join(words)))

    # Define domains for the letters (0-9 for most letters, 1-9 for the first letters)
    domains = {letter: list(range(10)) if letter != word1[0] and letter != word2[0] and letter != result[0] else list(range(1, 10)) for letter in letters}

    # Constraint for unique values
    def constraint_unique(variables, values):
        return len(values) == len(set(values))  # This removes repeated values and counts them

    # Constraint for addition
    def constraint_add(variables, values):
        def add_word(word):
            if len(word) == 0:  # This is the base case
                return ""
            else:
                return str(values[variables.index(word[0])]) + add_word(word[1:])
            
        factor1 = int(add_word(word1))
        factor2 = int(add_word(word2))
        result_factors = int(add_word(result))
        return (factor1 + factor2) == result_factors

    # Define the two constraints created earlier for the "letters"
    constraints = [
        (letters, constraint_unique),
        (letters, constraint_add),
    ]
    
    # Define the CSP problem
    problem = CspProblem(letters, domains, constraints)

    # Find the solution using backtracking
    solution = backtrack(problem)

    return solution

# Set up the Streamlit app
st.title("Cryptarithmetic Puzzle Solver Murrel Venlo")  # This sets the title of the web app in Streamlit
word1 = st.text_input("Enter word 1:", "TO")  # Create an input for the first word with a default value
word2 = st.text_input("Enter word 2:", "GO")  # Create a second input for the second word with a default value
result = st.text_input("Enter the result", "OUT")  # And an input for the result with a default value
solve_button = st.button("Solve")  # If this button is clicked, you get the solution

# Check if the 'Solve' button is pressed below
if solve_button:
    words = [word1, word2, result]  # Save the entered words in a list
    puzzle_input = f"{word1} + {word2} = {result}"  # Format the input as an arithmetic expression

    # Call the cryptarithmetic_solver function to find a solution
    solution = cryptarithmetic_solver(words)
    
    # Check if a solution is found
    if solution:
        st.success("Solution found:")  # Show a success message
        
        # Create the formatted equation (words only)
        formatted_equation_words = f"{word1} + {word2} = {result}"
        
        result = []
        added_letters = set()  # Create a set to keep track of added letters
        for word in words:
            for letter in word:
                if letter not in added_letters:
                    digit = solution[letter]
                    result.append([letter, digit])  # Add as [letter, digit]
                    added_letters.add(letter)  # Add the letter to the set

        # For a better display of the result, I used Pandas to create a DataFrame
        solution_df = pd.DataFrame(result, columns=["Letter", "Digit"])  # In my dataframe, I want a column with the letter and another with the digits
        
        # Build the equation with digits
        equation_with_digits = formatted_equation_words
        for _, row in solution_df.iterrows():
            equation_with_digits = equation_with_digits.replace(row["Letter"], str(row["Digit"]))
        
        # First, show the equation (words)
        st.write(formatted_equation_words)
        
        # Show the equation with digits on a new line
        st.write(equation_with_digits)
        
        # Display the solution in a DataFrame
        st.write(solution_df)
    else:
        st.warning("No solution found.")  # Show a warning message if no solution is found



# import streamlit as st
# from simpleai.search import CspProblem, backtrack
# import pandas as pd

# # Hier heb ik een functie om te controleren of een oplossing geldig is
# def is_valid_solution(variables, values):
#     # Zorg ervoor dat elke variabele een unieke en verschillende waarde heeft
#     if len(values) != len(set(values)):
#         return False
    
#     # Zorg ervoor dat getallen niet met nul beginnen
#     for word in words:
#         if values[variables.index(word[0])] == 0:
#             return False
    
#     # Vervang letters door waarden en controleer de juistheid van de rekenkundige bewerking
#     exp = puzzle_input
#     for i, letter in enumerate(variables):
#         exp = exp.replace(letter, str(values[i]))
    
#     try:
#         return eval(exp) == 0  # Hier evalueer ik de expressie en controleer of deze gelijk is aan nul
#     except ZeroDivisionError:
#         return False

# # Hier heb ik een functie om het cryptarithmetic puzzle op te lossen
# def cryptarithmetic_solver(words):

#     # Dit maakt een lijst van unieke letters uit de woorden
#     letters = list(set(''.join(words)))

#     # Definieer domeinen voor de letters (0-9 voor de meeste letters, 1-9 voor de eerste letters) (Het was of dit of gewoon voor alle letters een range definiëren)
#     domains = {letter: list(range(10)) if letter != word1[0] and letter != word2[0] and letter != result[0] else list(range(1, 10)) for letter in letters}

#     # Dit is een constraint voor unieke waarden
#     def constraint_unique(variables, values):
#         return len(values) == len(set(values))  # Dit verwijder herhaalde waarden en tel deze

#     # Dit is een constraint om op te tellen
#     def constraint_add(variables, values):
#         def add_word(word):
#             if len(word) == 0: # Dit is de Base case
#                 return ""
#             else:
#                 return str(values[variables.index(word[0])]) + add_word(word[1:])
            
#         factor1 = int(add_word(word1))
#         factor2 = int(add_word(word2))
#         result_factors = int(add_word(result))
#         return (factor1 + factor2) == result_factors

#     # Hier definieër de twee constraints die eerder heb aangemaakt voor de "letters"
#     constraints = [
#         (letters, constraint_unique),
#         (letters, constraint_add),
#     ]
    
#     # Definieer het CSP-probleem
#     problem = CspProblem(letters, domains, constraints)

#     # Vind de oplossing met behulp van backtracking
#     solution = backtrack(problem)

#     return solution

# # Stel de Streamlit-app in
# st.title("Cryptarithmetic Puzzle Solver Murrel Venlo")  # Dit stelt de titel van de web-app in streamlit voor
# word1 = st.text_input("Voer woord 1 in:", "TO")  # Ik maak een input voor het eerste woord met een standaardwaarde
# word2 = st.text_input("Voer woord 2 in:", "GO")  # Ik maak een tweede input voor het tweede woord met een standaardwaarde
# result = st.text_input("Voer het resultaat in", "OUT")  # En een input voor het resultaat met een standaardwaarde
# solve_button = st.button("Oplossen")  # Als op dit knopje klik, krijg je de oplossing

# # Hieronder controleer ik of de knop 'Oplossen' is ingedrukt
# if solve_button:
#     words = [word1, word2, result]  # Sla de ingevoerde woorden op in een lijst
#     puzzle_input = f"{word1} + {word2} = {result}"  # Formatteer de invoer als een rekenkundige expressie

#     # Roep de cryptarithmetic_solver-functie aan om een oplossing te vinden
#     solution = cryptarithmetic_solver(words)
    
#     # Controleer of een oplossing is gevonden
#     if solution:
#         st.success("Oplossing gevonden:")  # Toon een succesbericht
        
#         # Maak de geformatteerde vergelijking (alleen woorden)
#         formatted_equation_words = f"{word1} + {word2} = {result}"
        
#         result = []
#         added_letters = set()  # Maak een set om bijgehouden toegevoegde letters
#         for word in words:
#             for letter in word:
#                 if letter not in added_letters:
#                     digit = solution[letter]
#                     result.append([letter, digit])  # Voeg toe als [letter, cijfer]
#                     added_letters.add(letter)  # Voeg de letter toe aan de set

#         # Voor een betere weergave van het resultaat heb ik m.b.v. Pandas gebruik gemaakt van een DataFrame
#         solution_df = pd.DataFrame(result, columns=["Letter", "Cijfer"]) # In mijn dataframe wil een colum met de letter en de andere met de cijfers
        
#         # Bouw de vergelijking met cijfers
#         equation_with_digits = formatted_equation_words
#         for _, row in solution_df.iterrows():
#             equation_with_digits = equation_with_digits.replace(row["Letter"], str(row["Cijfer"]))
        
#         # Toon eerst de vergelijking (woorden)
#         st.write(formatted_equation_words)
        
#         # Toon de vergelijking met cijfers op een nieuwe regel
#         st.write(equation_with_digits)
        
#         # Toon de oplossing in een DataFrame
#         st.write(solution_df)
#     else:
#         st.warning("Geen oplossing gevonden.")  # Toon een waarschuwingsbericht als er geen oplossing is gevonden
