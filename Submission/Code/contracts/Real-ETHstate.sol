// SPDX-License-Identifier: CC0-1.0
pragma solidity ^0.8.0;

import {ERC4907} from "./ERC4907.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Burnable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract Real_ETHstate is ERC4907 /* ERC721Burnable, Ownable */ {
    struct PropertyInfo
    {
        /// @dev Address Line 1. E.g.: `Block C Unit 1, 234 Bridge Road Annandale NSW 2008 Australia`
        string street_address;

        /// @dev Land registry Lot / Plan number reference. E.g.: `1863/1000001`, or `35/G/5720` or `1/SP
        string lot_plan_number;

        /// @dev IPFS URI of the Property
        string property_uri;

        /// @dev Asking Rent - the weekly rent amount being requested (generally set by Owner of the Property)
        uint256 askingRent;

    }

    /// @dev create the mapping to Property Information based on a token for a property
    mapping (uint256  => PropertyInfo) internal _propertyInfo;

    uint256 private _nextTokenId;
    address public owner;

    modifier onlyOwner() {
        require(msg.sender==owner, "Real-ETHstate: You are not the owner");
        _;
    }

    constructor()
        ERC4907("Real-ETHstate", "RES")   
    {
        owner = msg.sender;
    }

    function safeMint(address to,
                      string memory street_address,
                      string memory lot_plan_number,
                      string memory property_uri) public onlyOwner {
        uint256 tokenId = _nextTokenId++;
        _safeMint(to, tokenId);

        _propertyInfo[tokenId] = PropertyInfo(street_address, lot_plan_number, property_uri, 0);

    }
}






