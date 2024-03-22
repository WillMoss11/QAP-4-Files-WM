
const MotelCustomer = { //could set up as a let to change the values for new customers
    //List for MotelCustomer 
    name: "Luke Skywalker",
    birthDate: new Date(1951, 9, 25), //Makes a date as 2002-1-12 
    gender: "Male",
    roomPreference: ["Non-smoking", "Pets Allowed", "Room Size", "Number of Beds", "Price", "Close Amenities", "Safety and Security", "Room Conditions", "Check-in/Check-out Times", "Reviews and Ratings", "Additional Services"],
    paymentMethod: "Credit Card",
    mailingAddress: {
        street: "250 Hoth Vader Ave",
        city: "Oakland", 
        province: "CA",
        country: "United States",
        postalCode: "A1L1L2"
      },
    phoneNumber: "1-709-999-9999",
    checkInDate: new Date(2024, 3, 13), // Makes a new date (YEAR, MONTH, DAY)
    checkOutDate: new Date(2024, 3, 24), // Makes a new date (YEAR, MONTH, DAY)

    getAge: function() {
        const today = new Date(); // Creates a new Date object representing the current date.
        let age = today.getFullYear() - this.birthDate.getFullYear(); // Calculation to get age.
        return age; // returns age.
    },

//To get the duration of stay.

    getDurationOfStay: function() {
        const millisecondsPerDay = 1000 * 60 * 60 * 24;
        const checkInTime = this.checkInDate.getTime();
        const checkOutTime = this.checkOutDate.getTime();
        const durationInMilliseconds = checkOutTime - checkInTime;
        return Math.ceil(durationInMilliseconds / millisecondsPerDay);
  } 
  
};
// The following list gets printed to the console.  
const customerDescription = `Name: ${MotelCustomer.name} 

Age: ${MotelCustomer.getAge()}

Gender: ${MotelCustomer.gender}

Room Preferences: ${MotelCustomer.roomPreference.join(', ')}

Payment Method: ${MotelCustomer.paymentMethod}

Mailing Address: ${MotelCustomer.mailingAddress.street}, ${MotelCustomer.mailingAddress.city}, ${MotelCustomer.mailingAddress.province}, ${MotelCustomer.mailingAddress.country}, ${MotelCustomer.mailingAddress.postalCode}

Phone Number: ${MotelCustomer.phoneNumber}

Check-In Date: ${MotelCustomer.checkInDate.toDateString()}

Check-Out Date: ${MotelCustomer.checkOutDate.toDateString()}

Duration of Stay: ${MotelCustomer.getDurationOfStay()} days`;



console.log(customerDescription); //sends to console

let customerDescriptionPara = `${MotelCustomer.name} is a ${MotelCustomer.gender}, with a dying passion to save the galaxy. On the other hand he is from ${MotelCustomer.mailingAddress.city}, ${MotelCustomer.mailingAddress.country}. ${MotelCustomer.name} also lives on ${MotelCustomer.mailingAddress.street}. Which is very Ironic. He has decided to stay in a motel and has a certain preference on the room he chooses. Starting with a ${MotelCustomer.roomPreference[0]} and ${MotelCustomer.roomPreference[1]} room. He also wants a spacious ${MotelCustomer.roomPreference[2]} plus good ${MotelCustomer.roomPreference[7]}. After his stay he will be sure to give some good ${MotelCustomer.roomPreference[9]}.`


console.log(customerDescriptionPara); //sends to console