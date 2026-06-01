import sys
from repository import LeadRepository, LeadNotFoundError, DuplicateLeadError

def print_menu():
    print("\n" + "="*30)
    print(" AcademyOps Lead Manager ")
    print("="*30)
    print("1. List all leads")
    print("2. Add a new lead")
    print("3. Update a lead's stage")
    print("4. Delete a lead")
    print("5. Exit")
    print("="*30)

def main():
    repo = LeadRepository()
    
    while True:
        print_menu()
        choice = input("Enter your choice (1-5): ")
        
        if choice == '1':
            leads = repo.list()
            if not leads:
                print("\n[!] No leads found in the database.")
            else:
                print("\nID | Name | Phone | Stage")
                print("-" * 40)
                for lead in leads:
                    print(f"{lead['id']} | {lead['name']} | {lead['phone']} | {lead['stage']}")
        
        elif choice == '2':
            print("\n--- Add New Lead ---")
            name = input("Name: ")
            phone = input("Phone: ")
            source = input("Source (e.g., Website, Ad): ")
            stage = input("Stage (New, Contacted, Qualified, Demo, Enrolled, Lost): ")
            try:
                lead_id = repo.create(name, phone, source, stage)
                print(f"\n[+] Success! Lead added with ID {lead_id}")
            except DuplicateLeadError as e:
                print(f"\n[x] Error: {e}")
            except Exception as e:
                print(f"\n[x] Database Error: {e}")
                
        elif choice == '3':
            print("\n--- Update Lead Stage ---")
            try:
                lead_id = int(input("Enter Lead ID: "))
                new_stage = input("Enter new stage: ")
                repo.update_stage(lead_id, new_stage)
                print("\n[+] Success! Stage updated.")
            except LeadNotFoundError as e:
                print(f"\n[x] Error: {e}")
            except ValueError:
                print("\n[x] Error: Please enter a valid number for ID.")
                
        elif choice == '4':
            print("\n--- Delete Lead ---")
            try:
                lead_id = int(input("Enter Lead ID to delete: "))
                repo.delete(lead_id)
                print("\n[-] Success! Lead deleted.")
            except LeadNotFoundError as e:
                print(f"\n[x] Error: {e}")
            except ValueError:
                print("\n[x] Error: Please enter a valid number for ID.")
                
        elif choice == '5':
            print("\nExiting AcademyOps. Goodbye!")
            sys.exit(0)
        else:
            print("\n[x] Invalid choice. Please select a number from 1 to 5.")

if __name__ == '__main__':
    main()