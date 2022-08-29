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

    dataHistory[] internal dHistory;
    AccessInfo[] internal webs;
    Data  private d;
    
    //First id is 1, 0 value is default  in mapping
    mapping (string => uint) stringToWebIndex;

    function setData1(address _wallet, string memory _email, string memory _dni, string memory _name,  string memory _surname, 
                    string memory _gender, uint _birthday, string memory _addr) public {
        d.wallet = _wallet; d.email = _email; d.dni = _dni; d.name = _name; d.surname = _surname; d.gender = _gender;  d.birthday = _birthday; d.addr = _addr;     } 

    function setData2 (string memory _city, string memory _postalCode, 
                    string memory _country, string memory _phoneNumber, string memory _ig, string memory _tw, string memory _creditCard) public {
       d.city = _city; d.postalCode = _postalCode; d.country = _country; d.phoneNumber = _phoneNumber; d.igUsername = _ig;  d.twUsername = _tw; d.creditCard = _creditCard;    }

    function getData() public view returns (Data memory){
        return d; //retrieve last user data registered
    }

    function saveData () public  {
        dHistory.push(dataHistory(d, block.timestamp));
    }

    function getHistory() public view returns (dataHistory[] memory) {
        return dHistory;
    }

    function addWeb(string memory _name, string[] memory _dataAccessed) public returns (bool) {

        if (!checkWebRegistered(_name)){
            uint[] memory access;
            if (checkEmptyWebs()){
                // Add genesis webInfo without info (index 0)
                string[] memory dataAux;
                webs.push(AccessInfo ("None", false, access, dataAux, 0));
            }
            stringToWebIndex[_name] = webs.length;
            webs.push(AccessInfo (_name, true, access, _dataAccessed, block.timestamp));
            return true;
        }
        return false;
    }

    function addAccess (string memory _name) public returns (bool){

        if (checkWebRegistered(_name)){
            if (checkWebConsent(_name)){
                webs[getWebIndex(_name)].access.push(block.timestamp);
                return true;
            }
        }
        return false;
    }

    function getAccess(string memory _name) public view returns (uint[] memory ){
        return getWebInfo(_name).access;
    }

    function getWebInfo(string memory _name) public view returns (AccessInfo memory){
        uint index = getWebIndex(_name);
        return webs[index];
    }

    function getWebIndex(string memory _name) internal view returns (uint) {
        return stringToWebIndex[_name];
    }

    function checkEmptyWebs () internal view returns (bool){
        return  webs.length == 0;
    }

    function checkWebConsent(string memory _name) public view returns (bool){

        if (checkWebRegistered(_name)){
            return getWebInfo(_name).permision;
        }
        return false;
    }  

    function checkWebRegistered (string memory _name) public view returns (bool){
        return getWebIndex(_name) > 0;
    }

    function getWebsInfo() public view returns (AccessInfo[] memory){
        return webs;
    }
}
