import './App.scss'
import { LeadForm } from './components/LeadForm'
import { FormProviderLead } from './providers/FormProvider'


function App() {

    return (
        <>
            <div className="container custom-max-width p-5">
                <h1 className='custom-pl'>Registrar Lead</h1>
                <FormProviderLead>
                    <LeadForm />
                </FormProviderLead>
            </div>
        </>
    )
}

export default App
