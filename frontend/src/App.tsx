import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { ChordProvider } from './store/ChordContext'
import { KeySignatureProvider } from './store/KeySignatureContext'
import MainLayout from './components/layout/MainLayout'
import KeyToChordsView from './components/features/KeyToChords/KeyToChordsView'
import ChordSubstitutionView from './components/features/ChordSubstitution/ChordSubstitutionView'
import ChordToNotesView from './components/features/ChordToNotes/ChordToNotesView'

function App() {
  return (
    <Router>
      <ChordProvider>
        <KeySignatureProvider>
          <MainLayout>
            <Routes>
              <Route path="/" element={<ChordSubstitutionView />} />
              <Route path="/key-to-chords" element={<KeyToChordsView />} />
              <Route path="/substitution" element={<ChordSubstitutionView />} />
              <Route path="/chord-to-notes" element={<ChordToNotesView />} />
            </Routes>
          </MainLayout>
        </KeySignatureProvider>
      </ChordProvider>
    </Router>
  )
}

export default App
