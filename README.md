<div align="center">
  
 ![logo](https://raw.githubusercontent.com/MarcosRamaR/controlTesoreria/refs/heads/master/Logo.PNG) 
 </div>

<div align="center">
  
![Badge en Desarollo](https://img.shields.io/badge/STATUS-EN%20DESAROLLO-red)
</div>

## Index

* [Description](#description)
* [Funcionalities](#functionalities)
* [Acceso al proyecto](#acceso)
* [Used Technologies](#used-technologies)
* [Developers](#developers)
* [License](#license)


## Description
Application for expense and income management and treasury forecasting. Mainly focused on the financial accounts of PYMEs or individuals.


## Functionalities


- `Expenses`: Screen to display, add, or remove planned expenses.
- `Incomes`: Screen to display, add, or remove planned incomes.
- `Forecast Charts`: Charts to display the projetion of upcoming transactions (30,60 and 90 days).
- `Control Charts`: Charts to show the balance and treasury evolution (quaterly and annually).
- `Expense Chart`: Chart to display expenses grouped by companies, showing their total expenditure.

## Known Issues

- Dates earlier than **1677-09-21** or later than **2262-04-11** may cause errors when processed, due to limitations of the `datetime64[ns]` type used by pandas.

## Access to the project

To use this application, you only need to run the .exe file included in the project. The first time the application is used, a .CSV file will be generated in the same folder where the .exe is located.
If you want to back up the data, simply copy that .csv file. Just keep in mind that the application requires the exact name of the generated file (treasury_record.csv) in order to retrieve the data from it.


## Used Technologies
  * Python</br>

### Main Libraries

- Pandas  
- Matplotlib

## Developers

<div align= "center">Marcos Rama </div>
<div align= "center">Email: marcos.rama.1994@gmail.com</div>

## License

<div align="center">
This project is open source and free to use. 
</div>
