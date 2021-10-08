import SwiftUI


struct CoachInfo: Codable {
    var ID: Int = 0
    var Name: String = ""
    var CoachGroup: String = ""
}


struct CoachInfoView: View {
    @State private var results = CoachInfo()
    
    var coachID: Int
    
    var body: some View {
        Form {
            Text("Name: \(results.Name)")
            Text("Group: \(results.CoachGroup)")
        }
        .onAppear(perform: getCoachInfo)
        .navigationTitle("Edit coach \(coachID)")
        .navigationBarTitleDisplayMode(.inline)
    }
    
    func getCoachInfo() {
        guard let url = URL(string: "http://local.IP.address:port_number/coach/\(coachID)") else {
            print("Invalid URL")
            return
        }
        
        let request = URLRequest(url: url)
        
        URLSession.shared.dataTask(with: request) { data, response, error in
            if let data = data {
                if let decodedResponse = try? JSONDecoder().decode(CoachInfo.self, from: data) {
                    DispatchQueue.main.async {
                        self.results = decodedResponse
                    }
                    return
                }
            }

            print("Fetch failed: \(error?.localizedDescription ?? "Unknown error")")
        }
        .resume()
    }
}
