import matplotlib.pyplot as plt
import pandas as pd

def bar_chart(response):
    if not isinstance(response, pd.DataFrame):
        print("Invalid response format. Expected Pandas DataFrame.")
        return

    # Assuming the DataFrame has at least two columns
    columns = response.columns
    if len(columns) < 2:
        print("Invalid response format. DataFrame must have at least two columns.")
        return

    # Extract data for plotting
    x_field = columns[0]
    y_field = columns[1]

    x_data = response[x_field]
    y_data = response[y_field].astype(float)

    # Bar chart
    plt.bar(x_data, y_data)
    plt.xlabel(x_field.capitalize())
    plt.ylabel(y_field.capitalize())
    plt.title(f'Top {x_field.capitalize()}s by {y_field.capitalize()}')
    plt.xticks(rotation=45, ha="right")  # Rotate X-axis labels for better readability
    plt.tight_layout()  # Adjust layout to prevent clipping of labels
    plt.show()
