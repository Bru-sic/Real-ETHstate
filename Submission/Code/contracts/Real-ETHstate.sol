// SPDX-License-Identifier: CC0-1.0
pragma solidity ^0.8.0;

import {ERC4907} from "./ERC4907.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Burnable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract Real_ETHstate is ERC4907 /* ERC721Burnable, Ownable */ {
    /// @dev Define the PropertyTypes enumeration. Note: enums are treated as a uint8 external to Solidity, with the first item's value being 0, followed by 1 etc
    enum PropertyTypes { NotSpecified, House, Townhouse, Apartment, Unit, Villa, Other }

    struct PropertyInfo
    {
        /// @dev Street Address of the property. E.g.: `Block C Unit 1, 234 Bridge Road Annandale NSW 2008 Australia`
        string street_address;

        /// @dev Land registry Lot / Plan number reference. E.g.: `1863/1000001`, or `35/G/5720` or `1/SP
        string lot_plan_number;

        /// @dev The type of property as an enumeration
        PropertyTypes property_type;

        /// @dev IPFS URI of the Property
        string property_uri;

        /// @dev rentInWei - the weekly rent amount in Wei being requested (attribute is managed by the Owner of the Property)
        uint256 rentInWei;

        /// @dev isRented - is the property currently rented out (attribute is managed by the Owner of the Property)
        bool isRented;
    
        /// @dev property_owner_eoa - Externally owned account (EOA) of the property owner
        address property_owner_eoa;

    }

    /// @dev create the mapping to Property Information based on a token for a property
    mapping (uint256  => PropertyInfo) internal _propertyInfo;

    uint256 private _nextTokenId;
    address public admin_eoa;

    /// @dev Modifier shortcut requiring the message sender to be the administrator. Restricts access to the function to Real-ETHstate Admins
    modifier onlyAdmin() {
        require(msg.sender==admin_eoa, "Real-ETHstate: You are not the administrator");
        _;
    }

    /// @dev Modifier shortcut requiring the message sender to be the property owner. Restricts access to the function to the property owner.
    modifier onlyPropertyOwner(uint256 tokenId) {
        //require(tokenId != address(0x0), "Real-ETHstate: Invalid address");
        
        require(msg.sender == GetPropertyOwner(tokenId), "Real-ETHstate: You are not the administrator");
        _;
    }
    
    constructor()
        ERC4907("Real-ETHstate", "RES")   
    {
        admin_eoa = msg.sender;
    }

    function safeMint(address to,
                      string memory street_address,
                      string memory lot_plan_number,
                      PropertyTypes property_type,
                      string memory property_uri) public onlyAdmin {
        uint256 tokenId = _nextTokenId++;
        _safeMint(to, tokenId);

        /// @dev Add the property attributes to the mapping but default the rent amount to 0 and set the status to not rented as the last 2 are for the property owner to manage
        _propertyInfo[tokenId] = PropertyInfo(street_address, lot_plan_number, property_type, property_uri, 0, false, to);

    }

    /// @notice getStreetAddress: Get the Street Address of the property. E.g.: `Block C Unit 1, 234 Bridge Road Annandale NSW 2008 Australia`
    /// @param tokenId Token Id of the property.
    /// @return Street Address of the specified property.
    function getStreetAddress(uint256 tokenId) public view returns (string memory) {
        return _propertyInfo[tokenId].street_address;
    }

    /// @notice getLotPlanRef: Get the Land registry Lot / Plan number reference. E.g.: `1863/1000001`, or `35/G/5720` or `1/SP
    /// @param tokenId Token Id of the property.
    /// @return Land registry Lot / Plan number reference of the specified property.
    function getLotPlanRef(uint256 tokenId) public view returns (string memory) {
        return _propertyInfo[tokenId].lot_plan_number;
    }

   /** @notice getPropertyType: returns the property type of the property specified by tokenId
        Since enum types are not part of the ABI, the signature of "getPropertyType"
     *  will automatically be changed to "getChoice() returns (uint8)"
     *  for all matters external to Solidity.
     */ 
    /// @param tokenId Token Id of the property.
    /// @return Property type of the specified property.
    function getPropertyType(uint256 tokenId) public view returns (PropertyTypes) {
        // **** Question for nick do we need to validate TokenId against boundaries?
        return _propertyInfo[tokenId].property_type;
    }

    /// @notice getPropertyURI: Get the PropertyURI returns the property URI of the property specified by tokenId
    /// @param tokenId Token Id of the property.
    /// @return PropertyURI of the specified property.
    function getPropertyURI(uint256 tokenId) public view returns (string memory) {
        return _propertyInfo[tokenId].property_uri;
    }


    /// @notice GetRentInWei - the weekly rent amount in Wei being requested (attribute is managed by the Owner of the Property)
    /// @param tokenId Token Id of the property.
    /// @return Weekly rent amount in Wei of the specified property.
    function GetRentInWei(uint256 tokenId) public view returns (uint256) {
        return _propertyInfo[tokenId].rentInWei;
    }


    /// @notice GetRentIsRented - whether the property is currently rented or not (attribute is managed by the Owner of the Property)
    /// @param tokenId Token Id of the property.
    /// @return Whether the specified property is currently rented or not.
    function GetRentIsRented(uint256 tokenId) public view returns (bool) {
        return _propertyInfo[tokenId].isRented;
    }

    /// @notice GetPropertyOwner - returns the EOA of the property owner
    /// @param tokenId Token Id of the property.
    /// @return Owner's externally owned account (EOA) of the specified property.
    function GetPropertyOwner(uint256 tokenId) public view returns (address) {
        return _propertyInfo[tokenId].property_owner_eoa;
    }

}
