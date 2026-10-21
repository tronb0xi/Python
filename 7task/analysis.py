import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def main():
    parser = argparse.ArgumentParser(description="Аналіз постачань фармацевтичної продукції")
    parser.add_argument('csv_file', type=str, nargs='?', default='supplies.csv', help='Шлях до вхідного CSV файлу')
    args = parser.parse_args()

    df = pd.read_csv(args.csv_file)

    df['total_price'] = df['quantity'] * df['price_per_unit']

    mean_price = np.mean(df['price_per_unit'])
    median_quantity = np.median(df['quantity'])
    std_price = np.std(df['price_per_unit'])

    supplier_profit = df.groupby('supplier')['total_price'].sum()
    top_supplier = supplier_profit.idxmax()

    category_quantity = df.groupby('category')['quantity'].sum()

    low_supply_filename = 'low_supply.csv'
    low_supply_df = df[df['quantity'] < 100]
    low_supply_df.to_csv(low_supply_filename, index=False)

    sorted_df = df.sort_values(by='total_price', ascending=False)
    print("Перші три рядки за загальною вартістю (total_price):")
    print(sorted_df.head(3))
    print("-" * 50)

    report_filename = 'report.txt'
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write("ЗВІТ З АНАЛІТИКИ ПОСТАЧАНЬ\n")
        f.write("=" * 30 + "\n")
        f.write(f"Середня ціна всіх препаратів: {mean_price:.2f}\n")
        f.write(f"Медіана кількості (quantity): {median_quantity}\n")
        f.write(f"Стандартне відхилення ціни (price_per_unit): {std_price:.2f}\n")
        f.write(f"Постачальник з найбільшим прибутком: {top_supplier}\n")
        f.write(f"Назва створеного файлу з дефіцитними поставками: {low_supply_filename}\n")

    plt.figure(figsize=(8, 5))
    category_quantity.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title('Розподіл кількості препаратів за категоріями')
    plt.xlabel('Категорія')
    plt.ylabel('Сумарна кількість')
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('category_distribution.png')
    plt.show()

if __name__ == '__main__':
    main()