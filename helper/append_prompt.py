import json
from rich.console import Console
from rich.prompt import Prompt
from rich import print
from rich.pretty import Pretty
from rich.panel import Panel

console = Console()

def print_panel(text, title=None):
    if title:
        panel = Panel(Pretty(text), title=f"[bold blue]{title}[/bold blue]", expand=False)
    else:
        panel = Panel(Pretty(text), expand=False)
    console.print(panel)

def add_prompt():
    console.print("[bold cyan]Welcome to the Prompt Creator![/bold cyan]\n")
    current_data = None
    # Open the json file and load the data
    with open('src/personas.json', 'r') as file:
        current_data = json.load(file)
    with open('helper/personas_backup.json', 'w') as file:
        json.dump(current_data, file, indent=4)
    # Ask the user for input and confirm each entry with a panel
    title = Prompt.ask("Enter the title of the new prompt")
    print_panel(title, "Title")
    
    # description = Prompt.ask("Enter the description of the new prompt")
    # print_panel(description, "Description")
    
    examples_input = Prompt.ask("Enter the examples of the new prompt (separate multiple examples with a comma)")
    examples = [example.strip() for example in examples_input.split(',')]  # Process examples
    print_panel(examples, "Examples")
    
    # symbol = Prompt.ask("Enter the symbol of the new prompt")
    # print_panel(symbol, "Symbol")
    
    console.print("Enter the system message of the new prompt (press enter twice when finished):")
    system_message_lines = []
    while True:
        line = input()
        if line:
            system_message_lines.append(line)
        else:
            break
    system_message = '\n'.join(system_message_lines)
    print_panel(system_message, "System Message")
    description = system_message[0:25]
    symbol = title[0:2]
    # Confirm the new prompt before adding
    new_prompt = {
        "title": title,
        "description": description,
        "examples": examples,
        "symbol": symbol,
        "systemMessage": system_message
    }
    # print_panel(new_prompt, "New Prompt Confirmation")
    


    # Add the new prompt to the existing data
    current_data[title] = new_prompt

    # Write the updated data back to the file
    
    print_panel(current_data[title], "Saved")
    
    confirm = Prompt.ask("Are you sure you want to add this prompt? (y/n)")

    # Ask the user if they want to undo the action
    if confirm.lower() == 'n':
        # Restore the data from the backup
        
        console.print("[bold red]No changes made.[/bold red]\n")
    else:
        with open('helper/personas_backup.json', 'w') as file:
            json.dump(current_data, file, indent=4)
        console.print("[bold blue]Backup saved to `helper/personas_backup.json` [/bold blue]\n\n")
        with open('src/personas.json', 'w') as file:
            json.dump(current_data, file, indent=4)
        console.print("[bold green]The new prompt has been successfully added.[/bold green]\n")

add_prompt()