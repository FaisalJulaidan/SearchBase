export const Validators = {

    isValidEmail: (email)=> {
        return /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email);
    },

    isValidTelephone: (telephone)=> {
        return /^((\+\d{1,3}(-| )?\(?\d\)?(-| )?\d{1,3})|(\(?\d{2,3}\)?))(-| )?(\d{3,4})(-| )?(\d{4})(( x| ext)\d{1,5}){0,1}$/.test(telephone);
    },

    isValidURL: (URL)=> {
        return /[-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?/.test(URL);
    },

    isValidString: (input)=> {
        return isNaN(input);
    },

    isValidNumber: (number)=> {
        return !(isNaN(number));
    },

    isValidFile: (fileName, types)=> {
        const getFileExt = fileName.substring(fileName.lastIndexOf('.') + 1).toLowerCase();
        return types.includes(getFileExt);  
   }
};