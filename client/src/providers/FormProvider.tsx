import { FormProvider} from "react-hook-form";
import { ReactNode } from "react";
import { useFormLead } from "../hooks/FormHelpers";


export const FormProviderLead = ({
    children,
}: {
    children: ReactNode
}) => {
    const methods = useFormLead()
    return <FormProvider {...methods}>{children}</FormProvider>
}

