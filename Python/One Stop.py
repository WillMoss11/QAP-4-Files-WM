# Description: Insurance Policy Management and Calculation for One Stop Insurance
# Name: William Moss
# Date(s): 03-19-2024


import string
from datetime import datetime, timedelta
import FormatValues as FV
import sys
import time


# Default Values



f = open('Defaults.dat', 'r')
NEXT_POLICY_NUMBER = int(f.readline())
BASIC_PREMIUM = float(f.readline())
ADDITIONAL_CAR_DISCOUNT = float(f.readline())
EXT_LIABILITY_COST_PER_CAR = float(f.readline())
GLASS_COVERAGE_COST_PER_CAR = float(f.readline())
LOANER_CAR_COST_PER_CAR = float(f.readline())
HST_RATE = float(f.readline())
MONTHLY_PAYMENT_PROCESSING_FEE = float(f.readline())
f.close()

# Validation Sets
ALLOWED_NAME_CHARACTERS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-.' ")
ALLOWED_NUMBERS = set("1234567890")
VALID_PROVINCES = {"AB", "BC", "MB", "NB", "NL", "NS", "ON", "PE", "QC", "SK", "NT", "NU", "YT"}
PHONE_NUMBER_LENGTH = 10
POSTAL_CODE_LENGTH = 6
NUM_PAYMENTS = 8

# Global Claims List
Claims = []  


# Input Functions

def is_valid_input(InputValue, ValiType):

    # Universal check for blank input    
    if not InputValue.strip():
        return False

    # Exits loop if no other validations needed. 
    elif ValiType == 'Empty':
        return True

    if ValiType == 'Name':
        # Checks if the input contains valid naming characters
        return set(InputValue).issubset(ALLOWED_NAME_CHARACTERS)

    elif ValiType == 'PhoneNum':
        # Checks if the input is numerical and exactly 10 digits
        return InputValue.isdigit() and len(InputValue) == PHONE_NUMBER_LENGTH

    elif ValiType == 'PostCode':
        # Canadian postal code format: alternating letters and digits with no spaces
        return len(InputValue) == POSTAL_CODE_LENGTH and \
               all(InputValue[i].isalpha() for i in range(0, 6, 2)) and \
               all(InputValue[i].isdigit() for i in range(1, 6, 2))

    elif ValiType == 'Date':
        # Date format: YYYY-MM-DD
        try:
            datetime.strptime(InputValue, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    elif ValiType == 'Province':
        # Checks if the input is a valid province
        return InputValue.upper().strip() in VALID_PROVINCES

    elif ValiType == 'YesNo':
        # Validate 'Y' or 'N' input, case-insensitive
        InputValue = InputValue.upper()
        return InputValue.upper() in {'Y', 'N'}

    elif ValiType == 'PosiInteger':
        # Checks if the input is a digit and its integer representation is greater than 0
        return InputValue.isdigit() and int(InputValue) > 0

    elif ValiType == 'PosiFloat':
        # New validation logic for positive float values
        try:
            return float(InputValue) > 0
        except ValueError:
            return False


    else:
        raise ValueError(f"Invalid validation type provided: {ValiType}")

def prompt_and_validate(PromptMess, ValiType, ErrorMess, InitValue=None):
 
        if InitValue is not None:
            if is_valid_input(InitValue, ValiType):
                return InitValue
            else:
                print(ErrorMess)

        while True:
            UserInput = input(PromptMess)
            if is_valid_input(UserInput, ValiType):
                return UserInput
            print(ErrorMess)

def collect_customer_info():

    # Prompt for first name, validate, and format.    
    FName = prompt_and_validate(
        "Enter customers first name: ", 
        'Name',
        "Invalid first name. Please use only allowed characters."
    ).title()


    # Prompt for last name, validate, and format.
    LName = prompt_and_validate(
        "Enter customers last name: ", 
        'Name',
        "Invalid last name. Please use only allowed characters."
    ).title()


    # Prompt for street address, ensure it's not empty, and capitalize appropriately.
    Address = prompt_and_validate(
        "Enter customers street address: ", 
        'Empty',  
        "Invalid address. Please ensure the address is not empty."
    )
    Address = string.capwords(Address)


    # Prompt for city, validate, and format.
    City = prompt_and_validate(
        "Enter customers city: ", 
        'Name',  
        "Invalid city name. Please use only allowed characters."
    ).title()


    # Prompt for province abbreviation, validate, and format to uppercase.
    Province = prompt_and_validate(
        "Enter customers province (XX): ", 
        'Province',
        "Invalid province. Please enter a valid abbreviation."
    ).upper()


    # Prompt for postal code, validate format, remove spaces, and convert to uppercase.
    PostCode = prompt_and_validate(
        "Please enter the postal code (X9X9X9): ", 
        'PostCode',
        "Invalid postal code format."
    ).upper().replace(" ", "")


    # Prompt for phone number, validate format.
    PhoneNum = prompt_and_validate(
        "Enter customers phone number (9999999999): ", 
        'PhoneNum',
        "Invalid phone number. Please enter a 10-digit numeric phone number."
    )


    # Prompt for the number of cars, validate as positive integer, and convert to int.
    NumCars = int(prompt_and_validate(
        "Enter the number of cars being insured: ", 
        'PosiInteger',  
        "Please enter a positive integer."
    ))


    # Prompt for insurance options, validate as yes or no.
    ExtLiability = prompt_and_validate("Do you want extra liability coverage? (Y/N): ", "YesNo", "Data Entry Error - Answer Yes or No by typing Y or N").upper()
    GlassCoverage = prompt_and_validate("Do you want glass coverage? (Y/N): ", "YesNo", "Data Entry Error - Answer Yes or No by typing Y or N").upper()
    LoanerCar = prompt_and_validate("Do you want a loaner car coverage?(Y/N): ", "YesNo", "Data Entry Error - Answer Yes or No by typing Y or N").upper()


    return {
        'FName': FName,
        'LName': LName,
        'Address': Address,
        'City': City,
        'Province': Province,
        'PostCode': PostCode,
        'PhoneNum': PhoneNum,
        'NumCars': NumCars,
        'ExtLiability': ExtLiability,
        'GlassCoverage': GlassCoverage,
        'LoanerCar': LoanerCar
    }

def get_claims():

    # Initialize an empty list to store claim data
    Claims = [] 

    # Start the loop to continuously prompt for claim data
    while True:
        UserInput = input("Enter claim number (or 'END' to finish): ")
        if UserInput.lower() == 'end':
            break

        # Validate the claim number.
        ClaimNum = prompt_and_validate(
            "Enter claim number: ", 
            "PosiInteger",
            "Invalid input. Please enter a valid claim number.",
            InitValue=UserInput
        )

        # Prompt and validate the claim date in MM-DD-YYYY format
        ClaimDate = prompt_and_validate("Enter claim date (YYYY-MM-DD): ", "Date", "Invalid date format or date. Please enter the date in YYYY-MM-DD format.")

        # Prompt and validate the claim amount as a positive float
        ClaimAmt = float(prompt_and_validate("Enter claim amount: $", "PosiFloat", "Invalid amount. Please enter a valid number."))

        # Check for an existing claim with the same number, either updating the exting claim or adding it to the list.
        ExistClaim = next((Claim for Claim in Claims if Claim['Number'] == ClaimNum), None)
        if ExistClaim:
            # Update the amount of the existing claim
            print(f"Duplicate claim number found. Updating amount for claim number {ClaimNum}.")
            ExistClaim['Amount'] = ClaimAmt 
        else:
            # If no duplicate, append the new claim data as a dictionary to the claims list
            Claims.append({'Number': ClaimNum, 'Date': ClaimDate, 'Amount': ClaimAmt})

    # Return the list of claim dictionaries
    return Claims

def get_payment_info():

    # Mapping from single-letter inputs to full-word descriptions of payment methods.
    PayMap = {'F': 'Full', 'M': 'Monthly', 'D': 'Down Pay'}

    # Continuously prompt the user until a valid payment method is selected.
    while True:
        PayLetter = input("Enter payment method (Full (F), Monthly (M), Down Pay (D) ): ").strip().upper()
        if PayLetter in PayMap:
            PayMethod = PayMap[PayLetter]
            break
        else:
            print("Invalid payment method. Please enter 'F', 'M', or 'D'.")

    # Initialize down payment to None
    DownPay = None

    # Prompt for down payment amount if 'Down Pay' option is selected.
    if PayMethod == 'Down Pay':
        while True:
            try:
                DownPay = input("Enter the amount of the down payment: $").strip()
                DownPay = float(DownPay)
                if DownPay < 0:
                    # Ensures down payment is a positive value.
                    print("The down payment cannot be negative. Please enter a positive value.")
                    continue
                break
            except ValueError:
                # Handle non-numeric input.
                print("Invalid amount. Please enter a numeric value.")

    # Return a tuple containing two elements
    return PayMethod, DownPay


# Calulation Functions

def calculate_insurance_premium(NumCars, ExtLiability, GlassCoverage, LoanerCar):

    # Initial premium calculation for all cars
    Premium = BASIC_PREMIUM + (BASIC_PREMIUM * (1 - ADDITIONAL_CAR_DISCOUNT) * (NumCars - 1))

    # Calculate extra charges
    # Calculate costs for selected coverages
    ExtLiabilityCost = EXT_LIABILITY_COST_PER_CAR * NumCars if ExtLiability == 'Y' else 0
    GlassCoverageCost = GLASS_COVERAGE_COST_PER_CAR * NumCars if GlassCoverage == 'Y' else 0
    LoanerCarCost = LOANER_CAR_COST_PER_CAR * NumCars if LoanerCar == 'Y' else 0

    # Add additional costs to the premium
    TotPremium = Premium + ExtLiabilityCost + GlassCoverageCost + LoanerCarCost

    # Return a dictionary with all values
    return {
        'Premium': Premium,
        'TotalPremium': TotPremium,
        'ExtLiabilityCost': ExtLiabilityCost,
        'GlassCoverageCost': GlassCoverageCost,
        'LoanerCarCost': LoanerCarCost,
    }

def calculate_total_cost(Premium):
  
    # Calculate the HST based on the given premium
    Hst = Premium * HST_RATE

    # Calculate the total cost by adding the HST to the premium
    TotCost = Premium + Hst

    # Returns a tuple containing two float values
    return Hst, TotCost

def calculate_monthly_payments(TotCost, PayMethod, DownPay=None):

    # No monthly payments are needed if the payment is made in full.        
    if PayMethod == 'Full':
        return None
    else:
        # Adjust the total cost by subtracting any down payment provided.
        AdjustedCost = TotCost - DownPay if DownPay else TotCost

        # Calculate monthly payments by dividing the adjusted cost by the number of payments
        MonPayment = (AdjustedCost / NUM_PAYMENTS) + MONTHLY_PAYMENT_PROCESSING_FEE

        # Returns the monthly payment as an amount, or none.
        return MonPayment


# Output Functions for FormatValues

def format_currency(Value):
    # Format a number as a currency.
    return "${:,.2f}".format(Value)

def format_date(DateValue):
    # Format a datetime object into a more user-friendly string.
    return DateValue.strftime('%Y-%m-%d')

def prepare_customer_info_display(CustInfo):

    # Combine first name and last name into a full name.
    FullName = f"{CustInfo.get('FName', '')} {CustInfo.get('LName', '')}"

    # Retrieve phone number; handle missing value with a default.
    PhoneNum = CustInfo.get('PhoneNum', '')

    # Combine city, province, and postal code into one formatted string.
    CityProv = f"{CustInfo.get('City', '')}, {CustInfo.get('Province', '')}, {CustInfo.get('PostCode')}"

    # Retrieve street Address; handle missing value with a default.
    Address = f"{CustInfo.get('Address', '')}"

    # Preparing display variables
    DisplayInfo = {
        "Full Name": FullName,
        "Phone Number": PhoneNum,
        "Street": Address,
        "City": CityProv
    }

    # Return a dictionary formatted for display
    return DisplayInfo

def generate_and_display_receipt(CustInfo, Claims, PremDetails, Hst, TotCost, PayMethod, DownPay, MonPayment, TotPremium):

    # Format policy number for display
    DisplayPolicyNumber = f"{NEXT_POLICY_NUMBER}"

    # Format current date and future payment dates using a datetime format helper
    DisplayInvoiceDate = format_date(datetime.now())

    # Calculate the first payment date as the first day of the next month
    DisplayFirstPaymentDate = format_date((datetime.now().replace(day=28) + timedelta(days=4)).replace(day=1))

    # Format financial figures using a currency format helper
    DisplayPremium = format_currency(PremDetails['Premium'])
    DisplayTotalCost = format_currency(TotCost)
    DisplayHST = format_currency(Hst)
    DisplayPaymentMethod = f"{PayMethod}"
    DisplayDownPayment = format_currency(DownPay) if DownPay else "N/A"
    DisplayMonthlyPayment = format_currency(MonPayment) if MonPayment else "N/A"

    # Format customer information for display
    DisplayCustInfo = prepare_customer_info_display(CustInfo)

     # Format additional premium costs
    DisplayExtraLiabilityCost = format_currency(PremDetails['ExtLiabilityCost'])
    DisplayGlassCoverageCost = format_currency(PremDetails['GlassCoverageCost'])
    DisplayLoanerCarCost = format_currency(PremDetails['LoanerCarCost'])
    DisplayTotalPremium = format_currency(TotPremium)

    # Format each claim for display, including claim number, date, and amount
    DisplayClaims = []
    for Claim in Claims:
        ClaimDateFormat = datetime.strptime(Claim['Date'], '%Y-%m-%d')
        DisplayClaims.append({
            'Number': Claim['Number'],
            'Date': format_date(ClaimDateFormat),
            'Amount': format_currency(Claim['Amount'])
        })

  # Print Results


    print(f"")
    print(f"")
    print(f"    ____________________________________________________________")
    print(f"   |         ------- One Stop Insurance Policy --------         |")
    print(f"   |                       Policy - #{DisplayPolicyNumber:<10s}                 |")
    print(f"   |    ----------------------------------------------------    |")
    print(f"   | ---------- Current Invoice Date -- {DisplayInvoiceDate:>10s} ------------ |")
    print(f"   | ----------   First Payment Date -- {DisplayFirstPaymentDate:>10s} ------------ |")             
    print(f"   |____________________________________________________________|")
    print(f"   |          ========  Customer Information  ========          |")
    print(f"   |                                                            |")
    for key, value in DisplayCustInfo.items():
        print(f"   | {key:>22s} -- {value:<33s}|")
    print(f"   |____________________________________________________________|")
    print(f"   |         ===========  Premium Details  ===========          |")
    print(f"   |                                                            |")
    print(f"   |  Number  of Cars  ----  {CustInfo['NumCars']}  ----  {DisplayPremium:>9s}                 |")
    print(f"   |  Extra Liability  ----  {CustInfo['ExtLiability']}  ----  {DisplayExtraLiabilityCost:>9s}                 |")   
    print(f"   |  Glass  Coverage  ----  {CustInfo['GlassCoverage']}  ----  {DisplayGlassCoverageCost:>9s}                 |")
    print(f"   |  Loaner Car       ----  {CustInfo['LoanerCar']}  ----  {DisplayLoanerCarCost:>9s}                 |")
    print(f"   |____________________________________________________________|")
    print(f"   |                                                            |")
    print(f"   |  Total Premium  -------------  {DisplayTotalPremium:>9s}                  |")
    print(f"   |  HST Charge  --------------- {DisplayHST:>9s}                      |")
    print(f"   |____________________________________________________________|")
    print(f"   |  Total Cost  ---------------  {DisplayTotalCost:>9s}                    |")
    print(f"   |____________________________________________________________|")
    print(f"   |              ======  Payment  Details  ======              |")
    print(f"   |                                                            |")
    if PayMethod != 'Full':
        print(f"   |          ----  Payment Method ----- {DisplayPaymentMethod:>9s} ----         |")
        print(f"   |          ----    Down Payment ----- {DisplayDownPayment:>9s} ----         |")
        print(f"   |          ---- Monthly Payment ----- {DisplayMonthlyPayment:>9s} ----         |")
    else:
        print(f"   |                 Payment Method: Full Payment               |")
    if Claims:
        print(f"   |____________________________________________________________|")
        print(f"   |              ======  Claim(s) Details  ========            |")
        print(f"   |                                                            |")
        print(f"   |              Claim #    Claim Date       Amount            |")
        print(f"   |------------------------------------------------------------|")
        for DisplayClaim in DisplayClaims:
            print(f"   |                {DisplayClaim['Number']:>5s},   {DisplayClaim['Date']:>10s},   {DisplayClaim['Amount']:>9s}            |")
    else:
        print(f"   |____________________________________________________________|")
        print(f"   |            ========  Claim(s) Details  ========            |")
        print(f"   |                                                            |")
        print(f"   |                   Claims History: N/A                      |")
        print(f"   |____________________________________________________________|")
    print(f"   |____________________________________________________________|")
    print(f"   |                                                            |")
    print(f"   |       Thank you for choosing One Stop Insurance Company    |")
    print(f"   |____________________________________________________________|")
    print(f"")
    print(f"")
    print(f"")
    print(f"")
    print(f"Your policy data for policy number {DisplayPolicyNumber} has been saved successfully.")
    print()

# Main Functions

def process_insurance_policy():

    global NEXT_POLICY_NUMBER

    print(f"")
    print(f"Processing Policy Number: {NEXT_POLICY_NUMBER}")
    print(f"")

 
    CustInfo = collect_customer_info()
    Claims = get_claims()

 
    PremDetails = calculate_insurance_premium(
        CustInfo['NumCars'],
        CustInfo['ExtLiability'],
        CustInfo['GlassCoverage'],
        CustInfo['LoanerCar']
    )
    City = ['City']
    Province = ['Province']
    PostCode = ['PostCode']

    TotPremium = PremDetails['TotalPremium']
    Hst, TotCost = calculate_total_cost(TotPremium)
    PayMethod, DownPay = get_payment_info()
    MonPayment = calculate_monthly_payments(TotCost, PayMethod, DownPay)

    generate_and_display_receipt(CustInfo, Claims, PremDetails, Hst, TotCost, PayMethod, DownPay, MonPayment, TotPremium)



    # Store data in Claims.dat

    for _ in range(5):  # Change to control no. of 'blinks'
        print('Saving claim data ...', end='\r')
        time.sleep(.3)  # To create the blinking effect
        sys.stdout.write('\033[2K\r')  # Clears the entire line and carriage returns
        time.sleep(.3)

    f = open("Claims.dat", "a")
    
    f.write("{}, ".format(CustInfo)) 
    f.write("{}, ".format(City)) 
    f.write("{}, ".format(Province)) 
    f.write("{}, ".format(PostCode)) 
    f.write("{}\n".format(PayMethod))
    f.write("{}\n".format(str(DownPay)))
    f.write("{}\n".format(str(PremDetails)))     
    f.write("{}\n".format(str(TotPremium))) 

    f.close()

    print()
    
    print()
    print("Claim data successfully saved ...", end='\r')
    time.sleep(1)  # To create the blinking effect
    sys.stdout.write('\033[2K\r')  # Clears the entire line and carriage returns

     
    NEXT_POLICY_NUMBER += 1    

def main():

    ContinueProcessing = True
    while ContinueProcessing:

        process_insurance_policy()

        UserDecision = prompt_and_validate("Process another insurance policy? (Y/N): ", "YesNo", "Please enter Y/N for Yes or No")
        if UserDecision.upper() != 'Y':
            ContinueProcessing = False
    # Housekeeping    
    print("Thank you for using the One Stop Insurance Company program.")

if __name__ == "__main__":
    main()