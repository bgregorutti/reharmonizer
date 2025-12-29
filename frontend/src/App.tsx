import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { ChordProvider } from './store/ChordContext'
import { KeySignatureProvider } from './store/KeySignatureContext'
import MainLayout from './components/layout/MainLayout'
import HomePage from './components/pages/HomePage'
import KeyToChordsView from './components/features/KeyToChords/KeyToChordsView'
import ChordSubstitutionView from './components/features/ChordSubstitution/ChordSubstitutionView'
import ChordToNotesView from './components/features/ChordToNotes/ChordToNotesView'
import ReharmonizerView from './components/features/Reharmonizer/ReharmonizerView'

function App() {
  return (
    <Router>
      <ChordProvider>
        <KeySignatureProvider>
          <MainLayout>
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/key-to-chords" element={<KeyToChordsView />} />
              <Route path="/substitution" element={<ChordSubstitutionView />} />
              <Route path="/chord-to-notes" element={<ChordToNotesView />} />
              <Route path="/reharmonizer" element={<ReharmonizerView />} />
            </Routes>
          </MainLayout>
        </KeySignatureProvider>
      </ChordProvider>
    </Router>
  )
}

export default App
