import csv
from repository import LeadRepository, DuplicateLeadError

def run_import(input_file, quarantine_file):
    repo = LeadRepository()
    
    stats = {'total': 0, 'imported': 0, 'skipped': 0, 'duplicates': 0}
    seen_phones = set()
    quarantined_rows = []

    try:
        with open(input_file, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                stats['total'] += 1
                
                # 1. Clean the text
                name = row.get('name', '').strip().title()
                phone = row.get('phone', '').strip()
                source = row.get('source', '').strip().title()
                stage = row.get('stage', '').strip().capitalize()
                
                # Fix weird source names
                if source.lower() in ['fb', 'face book']:
                    source = 'Facebook'
                elif source.lower() in ['ig', 'insta']:
                    source = 'Instagram'

                # Fix bad stages
                if stage not in ['New', 'Contacted', 'Qualified', 'Demo', 'Enrolled', 'Lost']:
                    stage = 'New' 
                    
                # 2. Check for missing info
                if not name or not phone:
                    row['rejection_reason'] = 'Missing required field'
                    quarantined_rows.append(row)
                    stats['skipped'] += 1
                    continue
                    
                # 3. Check for duplicates in this file
                if phone in seen_phones:
                    row['rejection_reason'] = 'Duplicate phone in this batch'
                    quarantined_rows.append(row)
                    stats['duplicates'] += 1
                    continue
                    
                seen_phones.add(phone)
                
                # 4. Save to Database
                try:
                    repo.create(name=name, phone=phone, source=source, stage=stage)
                    stats['imported'] += 1
                except DuplicateLeadError:
                    row['rejection_reason'] = 'Duplicate phone already in database'
                    quarantined_rows.append(row)
                    stats['duplicates'] += 1
                    
    except FileNotFoundError:
        print(f"Error: Could not find {input_file}")
        return

    # 5. Save the bad rows to a quarantine file
    if quarantined_rows:
        with open(quarantine_file, mode='w', encoding='utf-8', newline='') as f:
            fieldnames = list(quarantined_rows[0].keys())
            if 'rejection_reason' in fieldnames:
                fieldnames.remove('rejection_reason')
                fieldnames.append('rejection_reason')
            
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(quarantined_rows)

    # 6. Print the summary report
    print("\n" + "="*30)
    print(" IMPORT RECONCILIATION SUMMARY ")
    print("="*30)
    print(f"Total Rows Processed : {stats['total']}")
    print(f"Successfully Imported: {stats['imported']}")
    print(f"Skipped (Bad Data)   : {stats['skipped']}")
    print(f"Skipped (Duplicates) : {stats['duplicates']}")
    print("="*30)
    if quarantined_rows:
        print(f"[!] {len(quarantined_rows)} rejected rows saved to {quarantine_file}\n")

if __name__ == '__main__':
    run_import('data/messy_leads.csv', 'data/quarantine.csv')