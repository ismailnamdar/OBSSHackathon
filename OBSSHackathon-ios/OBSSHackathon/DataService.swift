//
//  DataService.swift
//  OBSSHackathon
//
//  Created by ismail on 05/05/2018.
//  Copyright © 2018 teqwise. All rights reserved.
//

import Foundation
import Firebase

let STORAGE_BASE = Storage.storage().reference()
let DB_BASE = Database.database().reference()

class DataService {
    
    static let ds = DataService()
    
    // DataBase References
    private var _REF_URL = DB_BASE.child("url")
    private var _REF_RESULT = DB_BASE.child("result")
    private var _REF_PLACES = DB_BASE.child("places")
    private var _REF_TRAINING = DB_BASE.child("training")
    
    // Storage References
    private var _REF_IMAGES = STORAGE_BASE.child("images")
    
    var REF_URL: DatabaseReference {
        return _REF_URL
    }
    
    var REF_RESULT: DatabaseReference {
        return _REF_RESULT
    }
    
    var REF_PLACES: DatabaseReference {
        return _REF_PLACES
    }
    
    var REF_TRAINING: DatabaseReference {
        return _REF_TRAINING
    }
  
    var REF_IMAGES: StorageReference {
        return _REF_IMAGES
    }

}
