import sys
import os
import pandas as pd

print("HW")

import pandas as pd

# initialise data of lists.
data = {'Name': ['Tom', 'nick', 'krish', 'jack'],
        'Age': [20, 21, 19, 18]}

# Create DataFrame
df = pd.DataFrame(data)

# Print the output.
print(df)

def f(x):
    if int(x) >= 21:
        y = 'Normal Employee'
    else:
        y = 'Experienced Employee'
    return y

df['position'] = df['Age'].apply(f)

print(df)