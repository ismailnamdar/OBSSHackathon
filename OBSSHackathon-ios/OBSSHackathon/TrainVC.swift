//
//  TrainVC.swift
//  OBSSHackathon
//
//  Created by ismail on 06/05/2018.
//  Copyright © 2018 teqwise. All rights reserved.
//

import UIKit
import Firebase

class TrainVC: UIViewController, UINavigationControllerDelegate, UIImagePickerControllerDelegate {

    @IBOutlet weak var imageView: UIImageView!
    @IBOutlet weak var label: UITextField!
    
    var imagePicker: UIImagePickerController!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        imagePicker =  UIImagePickerController()
        imagePicker.delegate = self
        //imagePicker.sourceType = .camera
        imagePicker.allowsEditing = true
    }
    
    func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [String : Any]) {
        imagePicker.dismiss(animated: true, completion: nil)
        imageView.image = info[UIImagePickerControllerOriginalImage] as? UIImage
    }
    
    @IBAction func imageTapped(_ sender: Any) {
        present(imagePicker, animated: true, completion: nil)
    }

    @IBAction func uploadTapped(_ sender: Any) {
        if let imgData = UIImageJPEGRepresentation(imageView.image!, 0.2){
            
            //let url = UUID().uuidString
            
            //let imgUid = url
            let metadata = StorageMetadata()
            metadata.contentType = "image/jpeg"
            print("Selam")
            DataService.ds.REF_PLACES.child("index").observeSingleEvent(of: .value, with: {(snapshot) in
                if snapshot.exists() {
                    print(snapshot)
                    if let id = snapshot.value as? Int{
                        print(id)
                        DataService.ds.REF_IMAGES.child(String(id) + "_default").putData(imgData, metadata: metadata, completion: {(metadata, error) in
                            if error == nil{
                                print("Successfully upload the image to Firebase storage")
                                
                                DataService.ds.REF_TRAINING.child(String(id)).setValue(true)
                                
                                DataService.ds.REF_PLACES.child(String(id)).setValue(["name": self.label.text])
                                
                                DataService.ds.REF_PLACES.child("index").setValue(id+1)
                                
                                let alertController = UIAlertController(title: "Success", message:
                                    "Image successfully uploaded. Thank you for your contribution.", preferredStyle: UIAlertControllerStyle.alert)
                                alertController.addAction(UIAlertAction(title: "Ok", style: UIAlertActionStyle.default,handler: nil))
                                
                                self.present(alertController, animated: true, completion: nil)
                                
                            }else{
                                // error
                                print("Unable to upload image to Firebase storage")
                            }
                        })
                    }
                }
            })
            
           
        }
        else {
            print("Else error")
        }
    }
}
