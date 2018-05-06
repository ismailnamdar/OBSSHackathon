//
//  ViewController.swift
//  OBSSHackathon
//
//  Created by ismail on 05/05/2018.
//  Copyright © 2018 teqwise. All rights reserved.
//

import UIKit
import Firebase
import OmiseSDK

class ViewController: UIViewController, UINavigationControllerDelegate, UIImagePickerControllerDelegate, CreditCardFormDelegate {
    
    @IBOutlet weak var indicator: UIActivityIndicatorView!
    @IBOutlet weak var indicatorLeft: UIActivityIndicatorView!
    @IBOutlet weak var imageView: UIImageView!
    @IBOutlet var previewView: UIView!
    @IBOutlet weak var resultView: RoundedCornerView!
    @IBOutlet weak var titleLbl: UILabel!
    @IBOutlet weak var descLbl: UILabel!
    @IBOutlet weak var priceLbl: UILabel!
    @IBOutlet weak var makePaymentButton: RoundedCornerButton!
    
    var imagePicker: UIImagePickerController!
    private let publicKey = "pkey_test_123"

    override func viewDidLoad() {
        super.viewDidLoad()
        
        makePaymentButton.isHidden = true
        indicator.isHidden = true
        indicatorLeft.isHidden = true
        
        indicator.startAnimating()
        indicatorLeft.startAnimating()
        
        imagePicker =  UIImagePickerController()
        imagePicker.delegate = self
        //imagePicker.sourceType = .camera
        imagePicker.allowsEditing = true
    }
    
    func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [String : Any]) {
        imagePicker.dismiss(animated: true, completion: nil)
        imageView.image = info[UIImagePickerControllerOriginalImage] as? UIImage
    }

    @IBAction func saveTapped(_ sender: Any) {
        indicatorLeft.isHidden = false
        
        if let imgData = UIImageJPEGRepresentation(imageView.image!, 0.2){
            
            let url = UUID().uuidString
            
            let imgUid = url
            let metadata = StorageMetadata()
            metadata.contentType = "image/jpeg"
            
            DataService.ds.REF_IMAGES.child(imgUid).putData(imgData, metadata: metadata, completion: {(metadata, error) in
                if error == nil{
                    print("Successfully upload the image to Firebase storage")
                    
                    DataService.ds.REF_URL.child(imgUid).setValue(true)
                    
                    let alertController = UIAlertController(title: "Success", message:
                        "Image successfully uploaded.", preferredStyle: UIAlertControllerStyle.alert)
                    alertController.addAction(UIAlertAction(title: "Ok", style: UIAlertActionStyle.default,handler: nil))
                    
                    self.present(alertController, animated: true, completion: nil)
                    
                    self.indicatorLeft.isHidden = true
                    self.indicator.isHidden = false
                    
                    DataService.ds.REF_RESULT.child(imgUid + "result").observe(.value, with: { (snapshot) in
                        if snapshot.exists() {
                            if let snap = snapshot.value as? String {
                                let image_id = snap
                                
                                let place_id_array = image_id.components(separatedBy: "_")
                                let place_id = place_id_array[0]
                                print(place_id)
                                
                                DataService.ds.REF_PLACES.child(place_id).observeSingleEvent(of: .value, with: { (snapshot) in
                                    if snapshot.exists() {
                                        if let snap = snapshot.value as? Dictionary<String, AnyObject> {
                                            if let name = snap["name"] as? String {
                                                self.titleLbl.text = name
                                            }
                                            
                                            if let price = snap["price"] as? String {
                                                self.priceLbl.text = price
                                                self.makePaymentButton.isHidden = false
                                            }
                                            
                                            if let desc = snap["desc"] as? String {
                                                self.descLbl.text = desc
                                            }
                                        }
                                    }
                                })
                                
                                DataService.ds.REF_IMAGES.child(image_id).getData(maxSize: 2 * 10240 * 10240, completion: { (data, error) in
                                    if error != nil {
                                        print("ISMO: Unable to download image from Firebase storage")
                                        self.indicator.isHidden = true
                                    } else {
                                        print("ISMO: Image downloaded from Firebase storage")
                                        if let imgData = data {
                                            if let img = UIImage(data: imgData) {
                                                self.resultView.image = img
                                            }
                                        }
                                        
                                        self.indicator.isHidden = true
                                    }
                                })
                            }
                        }
                    })
                }else{
                    // error
                    print("Unable to upload image to Firebase storage")
                    self.indicatorLeft.isHidden = true
                }
            })
        }
    }
    
    @IBAction func makePayment(_ sender: Any) {
        let closeButton = UIBarButtonItem(title: "Close", style: .done, target: self, action: #selector(dismissCreditCardForm))
        
        let creditCardView = CreditCardFormController.makeCreditCardForm(withPublicKey: publicKey)
        creditCardView.delegate = self
        creditCardView.handleErrors = true
        creditCardView.navigationItem.rightBarButtonItem = closeButton
        
        let navigation = UINavigationController(rootViewController: creditCardView)
        present(navigation, animated: true, completion: nil)
    }
    
    func dismissCreditCardForm() {
        dismiss(animated: true, completion: nil)
    }
    
    func creditCardForm(_ controller: CreditCardFormController, didSucceedWithToken token: OmiseToken) {
        self.dismissCreditCardForm()
        let alert = UIAlertController(title: "Completed",   message: "Payment success", preferredStyle: UIAlertControllerStyle.alert)
        alert.addAction(UIAlertAction(title: "Ok", style: .default, handler:{ (action) in
            //self.present(UserPacketsVC(), animated: true, completion: nil)
        }))
        present(alert, animated: true, completion: nil)
        // Sends `OmiseToken` to your server for creating a charge, or a customer object.
    }
    
    func creditCardForm(_ controller: CreditCardFormController, didFailWithError error: Error) {
        self.dismissCreditCardForm()
        let alert = UIAlertController(title: "Payment fail",   message: "", preferredStyle: UIAlertControllerStyle.alert)
        alert.addAction(UIAlertAction(title: "Ok", style: .default, handler:{ (action) in
            //self.dismiss(animated: true, completion: nil)
        }))
        present(alert, animated: true, completion: nil)
        // Only important if we set `handleErrors = false`.
        // You can send errors to a logging service, or display them to the user here.
    }
    
    @IBAction func cameraTapped(_ sender: Any) {
        present(imagePicker, animated: true, completion: nil)
    }
}

