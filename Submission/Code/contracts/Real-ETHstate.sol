// SPDX-License-Identifier: CC0-1.0
pragma solidity ^0.8.0;

import {ERC4907} from "./ERC4907.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Burnable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract MyToken is ERC4907 /* ERC721Burnable, Ownable */ {
    uint256 private _nextTokenId;
    address public owner;

    modifier onlyOwner() {
        require(msg.sender==owner, "You are not the owner");
        _;
    }

    constructor()
        ERC4907("Real-ETHstate", "RES")   
    {
        owner = msg.sender;
    }

    function safeMint(address to) public onlyOwner {
        uint256 tokenId = _nextTokenId++;
        _safeMint(to, tokenId);
    }
/*function _msgSender() internal view override(Context, ERC2771Context)
      returns (address sender) {
      sender = ERC2771Context._msgSender();
  }

  function _msgData() internal view override(Context, ERC2771Context)
      returns (bytes calldata) {
      return ERC2771Context._msgData();
  }
*/
}






