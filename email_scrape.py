import pyperclip
import re
import json

tekst = pyperclip.paste()


def scrape_phones(tekst): 
    #ten regex obsługuje większość formatów numerow telefonów poza (123-123-123)
    numberRegex = re.compile(r'''
        (?<!\d)                # Negative lookbehind to ensure the number is not preceded by a digit
        (?:\+48\s?)?           # Optional country code
        (?:\d{2}\s?)?          # Optional area code
        \d{3}                  # First part of the phone number
        (?:\s?\d{2,3}){2}      # Second and third parts of the phone number
        (?!\d)                 # Negative lookahead to ensure the number is not followed by a digit
    ''', re.VERBOSE)
    
    #regex uzupełniający dla numerow w formacie 123-123-123
    numberRegex1 = re.compile(r'''
        (?<!\d)                # Negative lookbehind to ensure the number is not preceded by a digit
        (?:\+\d\d)?            # Optional country code
        \d{3}-\d{3}-\d{3}      # Phone number in the format 123-123-123
        (?!\d)                 # Negative lookahead to ensure the number is not followed by a digit
    ''', re.VERBOSE) 

    #regex filtrujący numery REGON, które te mają 9 cyfr
    regonRegex = re.compile(r'REGON:\s?(\d{9})')  #filtr dla numerów REGON 

    wszystkie_numery = numberRegex.findall(tekst) + numberRegex1.findall(tekst)
    potencjalne_regony = regonRegex.findall(tekst)
    wynikowe_numery = [numer for numer in wszystkie_numery if numer not in potencjalne_regony]

    return(wynikowe_numery)

def scrape_regon(tekst): #ta funkcja wykorzystuje regonRegex (po co ma sie marnowac)
    regonRegex = re.compile(r'REGON:\s?(\d{9})')
    potencjalne_regony = regonRegex.findall(tekst)

    return potencjalne_regony

def scrape_email(tekst):
    mailRegex = re.compile(r'''
        [a-zA-Z0-9_.+]+       #name part 
        @                     # @ symbol 
        [a-zA-Z0-9_.+]+       # domain name part     
                     ''',re.VERBOSE)
    emails = mailRegex.findall(tekst)
    return emails

def scrape_bank(tekst):
     #28 1500 1126 1211 2010 3937 0000
     bankRegex = re.compile(r'\d\d\s?\d{4}\s?\d{4}\s?\d{4}\s?\d{4}\s?\d{4}\s?\d{4}')
     bank = bankRegex.findall(tekst)
     
     return bank

def zapisz_wyniki(plik_wyniki, wyniki):
        """Ta funkcja zapisze wyniki do pliku JSON"""
        try:
            with open(plik_wyniki, 'w', encoding='utf-8') as file: #otwieram plik w trybie zapisu 'w'i kodowaniem utf-8
                json.dump(wyniki, file, ensure_ascii=False, indent=4)  # Zapis wyników do JSON poprzez dump z odpowiednimi ustawieniami
                #ensure_ascii=False pozwala na zapisywanie polskich, indent=4 pozwala na zapisywanie w czytelnej formie
            print(f"\nWyniki zostały zapisane w pliku {plik_wyniki}.")
        except Exception as blad:  # Obsługa błędów zapisu
            print(f"Błąd podczas zapisywania wyników: {blad}")

wyniki_mail = scrape_email(tekst)
wyniki_numery = scrape_phones(tekst)
wyniki_REGON = scrape_regon(tekst)
wyniki_bank = scrape_bank(tekst)

print(f'Znaleziono {len(wyniki_mail)} maili,{len(wyniki_numery)} numerów tel,\
      \n{len(wyniki_REGON)} REGONÓW i {len(wyniki_bank)} kont bankowych!')
#słownik na potrzeby json
wyniki = {'Adresy mail':wyniki_mail, 'Numery tel': wyniki_numery, 'REGONy':wyniki_REGON, \
          'Nr_rachunków':wyniki_bank }
zapisz_wyniki('wyniki.json', wyniki)







