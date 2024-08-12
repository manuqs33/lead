import './App.scss'
import { LeadForm } from './components/LeadForm'
import { FormProviderLead } from './hooks/FormHooks'


function App() {

    return (
        <>
            <div className="container custom-max-width p-5">
                <FormProviderLead>
                    <LeadForm />
                </FormProviderLead>
            </div>
        </>
    )
}

export default App
