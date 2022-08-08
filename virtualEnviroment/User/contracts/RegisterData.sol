// SPDX-License-Identifier: MIT
pragma solidity 0.8.15;


contract RegisterData {

    struct Data {
        address wallet;
        string email;
        string dni;
        string name;
        string surname;
        string gender;
        uint birthday;
        string addr;
        string city;
        string postalCode;
        string country;
        string phoneNumber;
        string igUsername;
        string twUsername;
        string creditCard;
    }

    Data internal d;

    function setData1(address _wallet, string memory _email, string memory _dni, string memory _name,  string memory _surname, 
                    string memory _gender, uint _birthday, string memory _addr) public {
        d.wallet = _wallet; d.email = _email; d.dni = _dni; 
        d.name = _name; d.surname = _surname; d.gender = _gender; 
        d.birthday = _birthday; d.addr = _addr; 
    } 

    function setData2 (string memory _city, string memory _postalCode, 
                    string memory _country, string memory _phoneNumber, string memory _ig, string memory _tw, string memory _creditCard) public {
       d.city = _city; d.postalCode = _postalCode; d.country = _country;
       d.phoneNumber = _phoneNumber; d.igUsername = _ig; 
       d.twUsername = _tw; d.creditCard = _creditCard;
    }

    function getData() public view returns (Data memory){
        return d; //retrieve all data Blocks
    }
}
