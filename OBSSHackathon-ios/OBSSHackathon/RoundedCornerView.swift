//
//  RoundedCornerView.swift
//  OBSSHackathon
//
//  Created by ismail on 05/05/2018.
//  Copyright © 2018 teqwise. All rights reserved.
//

import UIKit

class RoundedCornerView: UIImageView {
    
    override func layoutSubviews() {
        layer.cornerRadius = 5
        clipsToBounds = true
    }
    
}
