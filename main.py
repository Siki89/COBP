import requests


class ExchangeRateAPI:
    BASE_URL = "https://api.exchangerate.host/latest"

    def get_rates(self, base_currency="EUR"):
        params = {
            "base": base_currency
        }

        response = requests.get(self.BASE_URL, params=params, timeout=10)
        data = response.json()

        if "rates" not in data:
            raise Exception("Nepodařilo se načíst kurzy měn.")

        return data["rates"]


class CurrencyConverter:
    def __init__(self, api_service):
        self.api_service = api_service
        self.rates = {}

    def update_rates(self, base_currency="EUR"):
        self.rates = self.api_service.get_rates(base_currency)

    def show_currencies(self):
        print("\nDostupné měny:")
        for currency in sorted(self.rates.keys()):
            print(currency)

    def convert(self, amount, from_currency, to_currency):
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()

        if from_currency not in self.rates:
            raise ValueError(f"Neznámá měna: {from_currency}")

        if to_currency not in self.rates:
            raise ValueError(f"Neznámá měna: {to_currency}")

        amount_in_eur = amount / self.rates[from_currency]
        converted_amount = amount_in_eur * self.rates[to_currency]

        return converted_amount


class Application:
    def __init__(self):
        self.api = ExchangeRateAPI()
        self.converter = CurrencyConverter(self.api)

    def run(self):
        print("=== Objektově orientovaný převodník měn ===")

        try:
            self.converter.update_rates()
            print("Kurzy byly úspěšně aktualizovány.")
        except Exception as error:
            print(f"Chyba při načítání kurzů: {error}")
            return

        while True:
            self.converter.show_currencies()

            try:
                amount = float(input("\nZadej částku: "))
                from_currency = input("Z jaké měny: ")
                to_currency = input("Na jakou měnu: ")

                result = self.converter.convert(
                    amount,
                    from_currency,
                    to_currency
                )

                print(
                    f"\n{amount:.2f} {from_currency.upper()} = "
                    f"{result:.2f} {to_currency.upper()}"
                )

            except ValueError as error:
                print(f"Chyba: {error}")

            again = input("\nChceš pokračovat? (ano/ne): ").lower()

            if again != "ano":
                print("Program ukončen.")
                break


if __name__ == "__main__":
    app = Application()
    app.run()
