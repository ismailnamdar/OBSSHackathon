//
//  RoundedCornerButton.swift
//  OBSSHackathon
//
//  Created by ismail on 05/05/2018.
//  Copyright © 2018 teqwise. All rights reserved.
//

import UIKit

class RoundedCornerButton: UIButton {
    
    override func awakeFromNib() {
        super.awakeFromNib()
        layer.shadowOpacity = 0.8
        layer.shadowRadius = 5.0
        layer.shadowOffset = CGSize(width: 1.0, height: 1.0)
        layer.cornerRadius = 3.0
    }
    
}
