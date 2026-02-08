import Header from '../components/Header';
import HeroSpotlight from '../components/dashboard/HeroSpotlight';

function App() {
  return (
    <div className="min-h-screen bg-black text-white selection:bg-pink-500/30">
      <Header />
      <main className="max-w-[1600px] mx-auto">
        <HeroSpotlight />
      </main>
    </div>
  );
}

export default App;