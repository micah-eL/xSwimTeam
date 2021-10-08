import SwiftUI


struct HomeView: View {
    var body: some View {
        NavigationView {
            List {
                NavigationLink(destination: SwimmersView()) {
                    Text("Swimmers")
                }
                NavigationLink(destination: CoachesView()) {
                    Text("Coaches")
                }
            }
            .navigationTitle("xSwimTeam")
        }
    }
}
