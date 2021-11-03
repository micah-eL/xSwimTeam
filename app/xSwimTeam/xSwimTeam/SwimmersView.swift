import SwiftUI


struct SwimmerList: Codable {
    var ID: Int
    var Name: String
}


struct SwimmersView: View {
    @State private var editMode: EditMode = .inactive
    @State private var searchText = ""
    @State private var results = [SwimmerList]()
    
    var body: some View {
        TabView {
            List (results, id: \.ID) { item in
                link(label: "\(item.ID): \(item.Name)", destination: SwimmerInfoView(swimmerID: item.ID))
            }
            .onAppear(perform: getSwimmerList)
            .tabItem {
                Image(systemName: "plus")
            }
        }
        .navigationTitle("Swimmers")
        .toolbar {
            EditButton()
        }
        .navigationBarTitleDisplayMode(.inline)
        .environment(\.editMode, $editMode)
    }
    
    private func link<Destination: View>(label: String, destination: Destination) -> some View {
        return NavigationLink(destination: destination) {
            Text(label)
        }
    }
    
    func getSwimmerList() {
        guard let url = URL(string: "http://local.IP.address:port_number/swimmer/0") else {
            print("Invalid URL")
            return
        }
        
        let request = URLRequest(url: url)
        
        URLSession.shared.dataTask(with: request) { data, response, error in
            if let data = data {
                if let decodedResponse = try? JSONDecoder().decode([SwimmerList].self, from: data) {
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
