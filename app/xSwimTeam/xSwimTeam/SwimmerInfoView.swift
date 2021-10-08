import SwiftUI


struct SwimmerInfo: Codable {
    var ID: Int = 0
    var Name: String = ""
    var Age: Int = 0
    var SwimmerGroup: String = ""
    var MainEvent: String = ""
}


struct SwimmerInfoView: View {
    @State private var results = SwimmerInfo()
    
    var swimmerID: Int
    
    var body: some View {
        Form {
            Text("Name: \(results.Name)")
            Text("Age: \(results.Age)")
            Text("Group: \(results.SwimmerGroup)")
            Text("Main event: \(results.MainEvent)")
        }
        .onAppear(perform: getSwimmerInfo)
        .navigationTitle("Edit swimmer \(swimmerID)")
        .navigationBarTitleDisplayMode(.inline)
    }
    
    func getSwimmerInfo() {
        guard let url = URL(string: "http://local.IP.address:port_number/swimmer/\(swimmerID)") else {
            print("Invalid URL")
            return
        }
        
        let request = URLRequest(url: url)
        
        URLSession.shared.dataTask(with: request) { data, response, error in
            if let data = data {
                if let decodedResponse = try? JSONDecoder().decode(SwimmerInfo.self, from: data) {
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
