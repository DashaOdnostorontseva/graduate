var dropdownElementList = [].slice.call(document.querySelectorAll('.dropdown-toggle'))
var dropdownList = dropdownElementList.map(function (dropdownToggleEl) {
  return new bootstrap.Dropdown(dropdownToggleEl)
})

window.cadespluginLoaded = false;
cadesplugin.then(function search () {
    window.cadespluginLoaded = true;
    return new Promise(function (resolve, reject) {
        cadesplugin.async_spawn(function* (args) {

            try {
                var oStore = yield cadesplugin.CreateObjectAsync("CAdESCOM.Store");

                yield oStore.Open(
                    cadesplugin.CADESCOM_CONTAINER_STORE,
                    cadesplugin.CAPICOM_MY_STORE,
                    cadesplugin.CAPICOM_STORE_OPEN_MAXIMUM_ALLOWED
                );

                var oCertificates = yield oStore.Certificates;
                var count = yield oCertificates.Count;

                const infos = [];

                for (i = 1; i <= count; i++) {
                    const cert = yield oCertificates.Item(i);
                        
                    cert.SubjectName.then((result)=>{                        
                        const INN = result.split('INN=').pop().split(',')[0];
                        infos.push(INN);
                    }).catch(() => console.warn('Сертификаты не найдены'))
                }

                fetch('/choose_cert', { method: 'POST', body: JSON.stringify({ value: infos }) })
                    .then(response => { if (response.ok) return response.json() })
                    .then(data => {
                        if (!data.message) { return document.getElementById("countNotFound").innerHTML = data.messageNotFound; }

                        document.getElementById("count").innerHTML = data.message;

                        cadesplugin.async_spawn(function* (args) {

                            var oStore = yield cadesplugin.CreateObjectAsync("CAdESCOM.Store");

                            yield oStore.Open(
                                cadesplugin.CADESCOM_CONTAINER_STORE,
                                cadesplugin.CAPICOM_MY_STORE,
                                cadesplugin.CAPICOM_STORE_OPEN_MAXIMUM_ALLOWED
                            );
                            
                            var oCertificates = yield oStore.Certificates;

                            let index = data.indexNum + 1;
                            var cert = yield oCertificates.Item(index);

                            const dataFilling = (data, elementId) => { //функция, на вход данные и айди
                                const element = document.createElement('p') 
                                element.innerText = data
                                document.getElementById(elementId).insertAdjacentElement('beforeend', element);
                            }

                            const dataValues = [ //массив промисов
                                cert.SerialNumber, 
                                cert.ValidFromDate,
                                cert.ValidToDate,
                                cert.IssuerName,
                                cert.SubjectName,
                            ];

                            Promise.all(dataValues)
                                .then(([serial, fromDate, toDate, issuerName, subjectName]) => {//деструктуризация
                                    fromDate = fromDate.replace('T',' ').split('.')[0];
                                    toDate = toDate.replace('T',' ').split('.')[0];
                                    issuerName = issuerName.replace(/\*|CN=|SN=|\$/g,'')

                                    dataFilling(serial, 'SerialNumber');
                                    dataFilling(fromDate, 'ValidFromDate');
                                    dataFilling(toDate, 'ValidToDate');
                                    dataFilling(issuerName, 'IssuerName');
                                    dataFilling(subjectName, 'Owner');

                                    const option = document.createElement('option')
                                    option.innerText = subjectName.replace(/\*|CN=|SN=|\$/g,'').split(',')[0]
                                    option.value = JSON.stringify({ serial, fromDate, toDate, issuerName, subjectName })
                                    document.getElementById("CertName").insertAdjacentElement('beforeend', option);
                                })

                                    


                            const certForm = document.getElementById('cert-form');//айди форрмы (элемент формы)

                            certForm.addEventListener('submit', async (e) => { //обработчик события самбмит (код внутри запускается после события е)
                                e.preventDefault();

                                const successModal = new bootstrap.Modal('#chooseCertModal')
                                const formData = new FormData(e.target); //обращаемся к нашей форме, на которой произошло событие

                                try {
                                    const response = await fetch('/write_cert', {
                                        method: 'POST',
                                        body: formData
                                    })
                                    if (response.status !== 200) throw new Error('Response status is not 200')

                                    const data = await response.json()
                                    if (!data || data.status !== 'success') throw new Error('Invalid data of data is missing')

                                    successModal.show()
                                } catch (e) { //тут е это ошибка
                                    console.warn(e.message);
                                }
                            })

                            var pKey = yield cert.PrivateKey;
                            var containerName = yield pKey.ContainerName;
                            let containerNameElement = document.createElement('p')
                            containerNameElement.innerText = containerName
                            document.getElementById("containerName").insertAdjacentElement('beforeend', containerNameElement); 
                        })
                    })
            } catch (err) {
                alert(cadesplugin.getLastError(err));
                console.log(err)
            }
        });
    }        
);});
