import requests
from dotenv import dotenv_values


# Functie: wisselkoersen opvragen gebaseerd op gekozen bronvaluta
def get_exchange_rates(api_key, base_currency):
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency.upper()}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if "conversion_rates" in data:
            return data["conversion_rates"]
        else:
            print("Fout: API gaf geen conversierates terug.")
            return None
    else:
        print(f"Fout: {response.status_code} - {response.text}")
        return None


# Functie: converteren
def convert(amount, rate):
    return amount * rate


def main():
    values = dotenv_values(".env")
    api_key = values["APIKEY"]

    print(f"Welkom bij de wisselkoers programma! Je hebt verschillende valuta's die je kan omrekenen.")


    while True:
        print("Beschikbare valuta: bijv. EUR, USD, GBP, JPY, CHF, AUD, CAD")

        # gebruiker kiest bronvaluta
        from_currency = input("Van welke valuta wil je omrekenen?: ").strip().upper()

        # Wisselkoersen ophalen
        rates = get_exchange_rates(api_key, from_currency)
        if rates is None:
            print("Ongeldige basisvaluta of API-probleem. Probeer opnieuw.")
            continue

        # gebruiker kiest doelvaluta
        to_currency = input(f"Naar welke valuta wil je {from_currency} omzetten?: ").strip().upper()

        if to_currency not in rates:
            print("Deze valuta wordt niet ondersteund door de API. Probeer opnieuw.")
            continue

        # bedrag
        try:
            amount = float(input(f"Voer het bedrag in {from_currency} in: ").strip())
            if amount <= 0:
                print("Bedrag moet groter zijn dan 0.")
                continue

        except ValueError:
            print("Ongeldige invoer. Geef een geldig getal.")
            continue

        # conversie uitvoeren
        rate = rates[to_currency]
        result = convert(amount, rate)

        print(f"{amount:.2f} {from_currency} = {result:.2f} {to_currency} (Rate: {rate:.4f})")

        # Vraag of de klant nog een berekening wilt maken
        antwoord = input("\nWil je nog een berekening maken? (ja/nee): ").lower()
        if antwoord == "nee":
            print("Bedankt voor het gebruiken van dit programma en tot ziens!")
            break
        elif antwoord != "ja":
            print("Ongeldige keuze, programma wordt afgesloten.")
            break
main()
