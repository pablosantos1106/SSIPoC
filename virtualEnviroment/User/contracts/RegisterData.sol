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
        string creditCard;
    }

    struct AccessInfo{
        string name;
        bool permision;
        uint256[] access;
        string[] dataAccessed;
        uint256 acceptionDate;
    }

    struct dataHistory {
        Data data;
        uint256 lastUpdate;
    }

    // address that deploys contract will be the owner 
    address owner;

    constructor() { 
        owner = msg.sender; 
    }

    dataHistory[] internal dHistory;
    AccessInfo[] internal webs;
    Data private d;
    
    //First id is 1, 0 value is default in mapping
    mapping (string => uint) stringToWebIndex;

    function setData1(address _wallet, string memory _email, string memory _dni, string memory _name,  string memory _surname, 
                    string memory _gender, uint _birthday, string memory _addr) public {
        require(msg.sender == owner);
        d.wallet = _wallet; d.email = _email; d.dni = _dni; d.name = _name; d.surname = _surname; d.gender = _gender;  d.birthday = _birthday; d.addr = _addr;     } 

    function setData2 (string memory _city, string memory _postalCode, string memory _country, string memory _phoneNumber, string memory _creditCard) public {
        require(msg.sender == owner);
        d.city = _city; d.postalCode = _postalCode; d.country = _country; d.phoneNumber = _phoneNumber; d.creditCard = _creditCard;    }

    // Owner function to get his personal data
    function getData() public view returns (Data memory){
        require(msg.sender == owner);
        return d; //retrieve last user data registered
    }

    function getWebsInfo() public view returns (AccessInfo[] memory){
    require(msg.sender == owner);
    return webs;
    }

    function getWallet (string memory _WebName) public view returns (address) {require(checkWebConsent(_WebName)); require(checkParameterConsent(_WebName, 'Wallet')); return d.wallet;}
    function getEmail  (string memory _WebName) public view returns(string memory)  {require(checkWebConsent(_WebName)); require(checkParameterConsent(_WebName, 'Email')) ; return d.email;}
    function getDni  (string memory _WebName) public view returns (string memory)  {require(checkWebConsent(_WebName)); require(checkParameterConsent(_WebName, 'Dni')) ; return d.dni;}
    function getName  (string memory _WebName) public view returns (string memory) {require(checkWebConsent(_WebName)); require(checkParameterConsent(_WebName, 'Name')) ; return d.name;}
    function getSurname  (string memory _WebName) public view returns (string memory)  {require(checkWebConsent(_WebName)); require(checkParameterConsent(_WebName, 'Surname')) ; return d.surname;}
    function getGender  (string memory _WebName) public view returns (string memory)  {require(checkWebConsent(_WebName)); require(checkParameterConsent(_WebName, 'Gender')) ; return d.gender;}
    function getBirthday  (string memory _WebName) public view returns (uint) {require(checkWebConsent(_WebName)); require(checkParameterConsent(_WebName, 'Birthday'));  return d.birthday;}
    function getAddress  (string memory _WebName) public view returns (string memory){require(checkWebConsent(_WebName)); require(checkParameterConsent(_WebName, 'Address'));  return d.addr;}
    function getCity  (string memory _WebName) public view returns (string memory){require(checkWebConsent(_WebName)); require(checkParameterConsent(_WebName, 'City')); return d.city;}
    function getPostalCode  (string memory _WebName) public view returns (string memory) {require(checkWebConsent(_WebName)); require(checkParameterConsent(_WebName, 'PostalCode')); return d.postalCode;}
    function getCountry  (string memory _WebName) public view returns(string memory)  {require(checkWebConsent(_WebName)); require(checkParameterConsent(_WebName, 'Country')); return d.country;}
    function getPhoneNumber  (string memory _WebName) public view returns (string memory){require(checkWebConsent(_WebName)); require(checkParameterConsent(_WebName, 'PhoneNumber')); return d.phoneNumber;}
    function getCreditCard  (string memory _WebName) public view returns (string memory){require(checkWebConsent(_WebName)); require(checkParameterConsent(_WebName, 'CreditCard')); return d.creditCard;}


    function saveData () public  {
        require(msg.sender == owner);
        dHistory.push(dataHistory(d, block.timestamp));
    }

    function getHistory() public view returns (dataHistory[] memory) {
        require(msg.sender == owner);
        return dHistory;
    }

    function addWeb(string memory _Webname, string[] memory _dataAccessed) public {
        require (!checkWebRegistered(_Webname));
            uint[] memory access;
            if (checkEmptyWebs()){
                // Add genesis webInfo without info (index 0)
                string[] memory dataAux;
                webs.push(AccessInfo ("None", false, access, dataAux, 0));
            }
            stringToWebIndex[_Webname] = webs.length;
            webs.push(AccessInfo (_Webname, true, access, _dataAccessed, block.timestamp));
        }

    function addAccess (string memory _Webname) public returns (bool){
        if (checkWebRegistered(_Webname)){
            if (checkWebConsent(_Webname)){
                webs[getWebIndex(_Webname)].access.push(block.timestamp);
                return true;
            }
        }
        return false;
    }

    function getWebParams(string memory _Webname) public view returns (string[] memory ){
    require(msg.sender == owner);
    return getWebInfo(_Webname).dataAccessed;
    }

    function getWebInfo(string memory _Webname) public view returns (AccessInfo memory){
        require(msg.sender == owner);
        uint index = getWebIndex(_Webname);
        return webs[index];
    }

    function getWebIndex(string memory _Webname) internal view returns (uint) {
        return stringToWebIndex[_Webname];
    }

    function checkEmptyWebs () internal view returns (bool){
        return  webs.length == 0;
    }

    function checkWebConsent(string memory _Webname) public view returns (bool){
        if (checkWebRegistered(_Webname)){
            return getWebInfo(_Webname).permision;
        }
        return false;
    }  

    function checkWebRegistered (string memory _Webname) public view returns (bool){
        return getWebIndex(_Webname) > 0;
    }

    function checkParameterConsent (string memory _webName, string memory parameter) internal view returns (bool){
        string[] memory params = getWebParams(_webName);
        for (uint i=0; i < params.length; i++) {
            if ((keccak256(abi.encodePacked(params[i]))) == (keccak256(abi.encodePacked(parameter)))){
                return true;
            }
        }
        return false;
    }
}
