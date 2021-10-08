import SwiftUI


struct CoachList: Codable {
    var ID: Int
    var Name: String
}


struct CoachesView: View {
    @State private var results = [CoachList]()
    
    var body: some View {
        List (results, id: \.ID) { item in
            link(label: "\(item.ID): \(item.Name)", destination: CoachInfoView(coachID: item.ID))
        }
        .onAppear(perform: getCoachList)
        .navigationBarItems(trailing: Button(action: {}) {
            Image(systemName: "plus")
                .resizable()
                .padding(6)
                .background(Color.blue)
                .clipShape(Circle())
                .foregroundColor(.white)
        })
        .navigationBarTitleDisplayMode(.inline)
    }
    
    private func link<Destination: View>(label: String, destination: Destination) -> some View {
        return NavigationLink(destination: destination) {
            Text(label)
        }
    }
    
    func getCoachList() {
        guard let url = URL(string: "http://local.IP.address:port_number/coach/0") else {
            print("Invalid URL")
            return
        }
        
        let request = URLRequest(url: url)
        
        URLSession.shared.dataTask(with: request) { data, response, error in
            if let data = data {
                if let decodedResponse = try? JSONDecoder().decode([CoachList].self, from: data) {
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
