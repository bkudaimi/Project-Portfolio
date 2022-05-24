'''
HPLC Data Analysis Assistant (DANA), for BioConsortia Inc.
Windows 7 version 
This application grabs HPLC files from the specified folder, sorts them into three categories, and outputs bar charts.
Input: Name of a folder containing HPLC files exported as Excel files.
Output: Five bar charts of lipopeptide peak areas for each sample and one Excel file containing the peak area values.
Author: Bilal Kudaimi
2021-03-12
'''

def DANA(directory):
    #Importing the necessary libraries
    import matplotlib.pyplot as plt
    import os
    from pathlib import Path
    import pandas as pd
    import warnings
    import xlrd
    warnings.filterwarnings('ignore')

    try:
        #Converting function input into a string
        directory = str(directory)

        #Using the input to generate a path name
        directory_str = 'C:\\Users\\Bioconsortia Inc\\Desktop\\HPLC Export Files\\{}\\'.format(directory)
        l = os.listdir(directory_str)
        #Getting the file names inside the specified folder
        file_names = [x.split('.')[0] for x in l if x.endswith('.xls')]

        # Grabbing all sample names within the directory
        samples_list = []
        #Keep this line of code just in case. pathlist = Path(directory_str).rglob('*.xls')
        pathnames = []
        for item in l:
            if item.endswith('.xls'):
                pathnames.append(directory_str + item)

        #Reading each sample
        for path in pathnames:
            path_in_str = str(path)
            wb = xlrd.open_workbook(path_in_str, logfile = open(os.devnull, 'w'))
            samples_list.append(pd.read_excel(wb, 'Integration')[41:])


    except:
        print('Sorry, I could not find that directory')

    try:
        # Specifying the column names in the Excel files
        new_list = []
        for isolate in samples_list:
            isolate.rename(columns={'Chromatogram and Results': 'No.', 'Unnamed: 1': 'Peak Name',
                                    'Unnamed: 2': 'Retention Time (min)', 'Unnamed: 3': 'Area (mAU*min)',
                                    'Unnamed: 4': 'Height (mAU)', 'Unnamed: 5': 'Relative Area %',
                                    'Unnamed: 6': 'Relative Height %', 'Unnamed: 7': 'Amount'}, inplace=True)
            new_list.append(isolate[isolate['No.'] != 'n.a.'])

        # Splitting the data by retention time into iturins (<10.3), fengycins (10.3<x<17.3), and surfactins (>17.3)
        iturin = []
        fengycin = []
        surfactin = []
        for each in new_list:
            each.drop(each.tail(1).index, inplace=True)
            iturins = each[each['Retention Time (min)'] <= 10.3]['Area (mAU*min)'].sum()
            fengycins = each[(each['Retention Time (min)'] < 17.3) & (each['Retention Time (min)'] > 10.3)][
                'Area (mAU*min)'].sum()
            surfactins = each[each['Retention Time (min)'] >= 17.3]['Area (mAU*min)'].sum()

            iturin.append(iturins)
            fengycin.append(fengycins)
            surfactin.append(surfactins)

        temp = [sum(x) for x in zip(iturin, fengycin)]
        temp2 = [sum(y) for y in zip(temp, surfactin)]

        #Displaying the exact values of the lipopeptide peak areas for each sample
        df = pd.DataFrame({'Iturins': iturin, 'Fengycins': fengycin, 'Surfactins': surfactin, 'Total': temp2},
                          index=file_names)

        print(df)

        #Saving said values to an Excel file on the HPLC computer desktop.
        df.to_excel('C:\\Users\\BioConsortia Inc\\Desktop\\DANA Output Files\\' + directory + '.xlsx', engine='xlsxwriter')




        # Plotting the iturins, fengycins, surfactins, and total lipopeptides for each sample
        plt.bar(file_names, iturin)
        plt.xlabel('Samples')
        plt.ylabel('Peak Area (mAU*min)')
        plt.title('Iturin Peak Areas per Sample')
        plt.xticks(fontsize=7, rotation=90)
        plt.show()

        plt.bar(file_names, fengycin)
        plt.xlabel('Samples')
        plt.ylabel('Peak Area (mAU*min)')
        plt.title('Fengycin Peak Areas per Sample')
        plt.xticks(fontsize=7, rotation=90)
        plt.show()

        plt.bar(file_names, surfactin)
        plt.xlabel('Samples')
        plt.ylabel('Peak Area (mAU*min)')
        plt.title('Surfactin Peak Areas per Sample')
        plt.xticks(fontsize=7, rotation=90)
        plt.show()

        plt.bar(file_names, temp2)
        plt.xlabel('Samples')
        plt.ylabel('Peak Area (mAU*min)')
        plt.title('Total Peak Areas per Sample')
        plt.xticks(fontsize=7, rotation=90)
        plt.show()

        df.plot.bar()
        plt.xlabel('Samples')
        plt.ylabel('Peak Area (mAU*min)')
        plt.title('All Peak Areas per Sample')
        plt.xticks(fontsize=7, rotation=90)
        plt.show()

    except:
        print('Something went wrong!')


#Generating the console text displayed to the user
def main():
    count = 0
    print('My name is DANA, your HPLC data analysis assistant.')
    while count == 0:
        directory = input('Please enter the folder name where your HPLC excel data is stored: ')
        DANA(directory)
        mid_var = input('Would you like to analyze another experiment? (Y/N) ')
        if mid_var.upper() == 'Y' or mid_var.upper() == 'YES'.upper() or mid_var == 'Yes':
            continue
        elif mid_var.upper() == 'N' or mid_var.upper() == 'NO'.upper() or mid_var == 'No':
            count += 1
        else:
            print("I'll pretend your said yes.")
    end_var = input('Glad I could assist you today. Please press ENTER to exit.')

#Line that activates the function
if __name__ == '__main__':
    main()
