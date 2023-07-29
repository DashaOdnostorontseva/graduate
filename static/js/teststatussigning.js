let dropdownElementList = [].slice.call(
  document.querySelectorAll(".dropdown-toggle")
);
let dropdownList = dropdownElementList.map(function (dropdownToggleEl) {
  return new bootstrap.Dropdown(dropdownToggleEl);
});

fetch("/cert_option")
  .then((response) => response.json())
  .then((data) => {
    if (!data.mycerts) {
      alert("В вашем личном кабинете сертификаты не найдены");
    }
    let myValue = data.mycerts;
    myValue = myValue.toString();
    myValue = myValue.replace(/\*|CN=|SN=|\$/g, "").split(",")[0];
    let option = document.createElement("option");
    option.innerText = myValue;
    document
      .getElementById("CertName")
      .insertAdjacentElement("beforeend", option);
  });

const pathDoc = document.getElementById("pathDoc").value;
const pathDocName = pathDoc.replace("files/", "");

const getZip = async () => {
  try {
    const response = await fetch("/get_file", {
      method: "POST",
      body: JSON.stringify({ pathDoc: pathDoc }),
    });

    if (response.status !== 200) throw new Error("Status is not 200");

    const blob = await response.blob();

    return { file: new File([blob], "archive.zip"), fileName: pathDocName };
  } catch (e) {
    console.warn(e.message);
  }
};

const getFileFromZip = async () => {
  const jsZip = new JSZip();
  const { file, fileName } = await getZip(); //деструктуризация

  const zip = await jsZip.loadAsync(file);
  const fileFromZip = zip.files[`${fileName}`]; //объект типа файла, еще не сам файл (не конструкктор файла)
  const fileBlob = await fileFromZip.async("blob"); //преобразовываем объект предыдущий к блобу

  return new File([fileBlob], fileFromZip.name, {
    lastModified: fileFromZip.date,
  });
};

window.addEventListener("DOMContentLoaded", async () => {
  //ждем пока загрузится ДОМ и потом запускаем дальше

  window.cadespluginLoaded = false;
  cadesplugin.then(function search() {
    window.cadespluginLoaded = true;
    return new Promise(function (resolve, reject) {
      cadesplugin.async_spawn(function* (args) {
        let CADESCOM_CADES_BES = 1;
        let CAPICOM_CURRENT_USER_STORE = 2;
        let CAPICOM_MY_STORE = "My";
        let CAPICOM_STORE_OPEN_MAXIMUM_ALLOWED = 2;
        let CAPICOM_CERTIFICATE_FIND_SUBJECT_NAME = 1;
        let CADESCOM_BASE64_TO_BINARY = 1;
        let CAPICOM_AUTHENTICATED_ATTRIBUTE_SIGNING_TIME = 0;

        function ConvertDate(date) {
          switch (navigator.appName) {
            case "Microsoft Internet Explorer":
              return date.getVarDate();
            default:
              return date;
          }
        }

        const podpisForm = document.getElementById("podpis-form");

        podpisForm.addEventListener("submit", async (e) => {
          e.preventDefault();

          run(e);
        });

        let idDoc = document.getElementById("idDoc").value;
        console.log(idDoc);

        const formSubmit = async (e, message, oFile) => {
          const saveModal = new bootstrap.Modal("#saveModal");
          const blob = new Blob([message], { type: "text/plain" });
          const zip = new JSZip();

          const sendDataToDb = async (docSign) => {
            const formData = new FormData(e.target);

            formData.append("doc_sign", docSign);
            formData.append("status", "Подписан");
            formData.append('idDoc', idDoc);

            try {
              const response = await fetch("/myp", {
                method: "POST",
                body: formData,
              });

              const data = await response.json();

              if (data.status !== "success") {
                throw new Error("Send Error");
                return;
              }
            } catch (e) {
              console.warn(e.message);
            }
          };

          let zipContent = null;

          zip.file(pathDocName, oFile, { base64: true });
          zip.file(pathDocName + ".sig", message, { base64: true });

          zip
            .generateAsync({ type: "blob" })
            .then((content) => {
              zipContent = new File([content], pathDocName + ".zip", {
                type: content.type,
              });
            })
            .then(() => {
              saveModal.show();

              document
                .getElementById("saveFileButton")
                .addEventListener("click", () => {
                  sendDataToDb(zipContent).then(() => {
                    const fileName = pathDocName + ".zip";
                    const postData = async (url, file) => {
                      const formData = new FormData();
                      formData.append("file", file, fileName);
                      const response = await fetch(url, {
                        method: "POST",
                        body: formData,
                      });
                      return response;
                    };

                    postData("/validate", zipContent)
                      .then((response) => {
                        if (response.ok) {
                          saveAs(zipContent, pathDocName + ".zip");
                          saveModal.hide();
                        } else {
                          console.log(
                            "Подпись не прошла верификацию на сервере"
                          );
                          alert(
                            "Произошла ошибка на сервере. Попробуйте подписать и отправить документ еще раз"
                          );
                        }
                      })
                      .catch((error) => {
                        console.log("Error:", error);
                      });
                  });
                });

              document
                .querySelector(".btn-close")
                .addEventListener("click", () => {
                  sendDataToDb(zipContent).then(() => {
                    const fileName = pathDocName + ".zip";
                    const postData = async (url, file) => {
                      const formData = new FormData();
                      formData.append("file", file, fileName);
                      const response = await fetch(url, {
                        method: "POST",
                        body: formData,
                      });
                      return response;
                    };

                    postData("/validate", zipContent)
                      .then((response) => {
                        if (response.ok) {
                          window.location.href = "/";
                        } else {
                          console.log(
                            "Подпись не прошла верификацию на сервере"
                          );
                          alert(
                            "Произошла ошибка на сервере. Попробуйте подписать и отправить документ еще раз"
                          );
                        }
                      })
                      .catch((error) => {
                        console.log("Error:", error);
                      });
                  });
                });
            });

          document
            .getElementById("dontSaveFileButton")
            .addEventListener("click", () => {
              sendDataToDb(zipContent).then(() => {
                const fileName = pathDocName + ".zip";
                const postData = async (url, file) => {
                  const formData = new FormData();
                  formData.append("file", file, fileName);
                  const response = await fetch(url, {
                    method: "POST",
                    body: formData,
                  });
                  return response;
                };

                postData("/validate", zipContent)
                  .then((response) => {
                    if (response.ok) {
                      window.location.href = "/";
                    } else {
                      console.log("Подпись не прошла верификацию на сервере");
                      alert(
                        "Произошла ошибка на сервере. Попробуйте подписать и отправить документ еще раз"
                      );
                    }
                  })
                  .catch((error) => {
                    console.log("Error:", error);
                  });
              });
            });
        };

        function run(event) {
          cadesplugin.async_spawn(function* (args) {
            // Проверяем, работает ли File API
            if (window.FileReader) {
              // Браузер поддерживает File API.
            } else {
              alert(
                "Невозможно подписать документ в данном браузере, воспользуйтесь другим браузером"
              );
            }

            let reader = new FileReader();

            if (typeof reader.readAsDataURL != "function") {
              alert("Метод readAsDataURL() не поддерживается в FileReader.");
              return;
            }

            getFileFromZip().then((file) => {
              let oFile = reader.readAsDataURL(file);

              reader.onload = function (oFREvent) {
                cadesplugin.async_spawn(function* (args) {
                  let header = ";base64,";
                  let sFileData = oFREvent.target.result;
                  let sBase64Data = sFileData.substr(
                    sFileData.indexOf(header) + header.length
                  );
                  let oCertName = document.getElementById("CertName");
                  let sCertName = oCertName.value; // Здесь следует заполнить SubjectName сертификата
                  if ("" === sCertName) {
                    alert(
                      "Вы не выбрали сертификат. Для подписания необходимо выбрать сертификат из списка"
                    );
                    return;
                  }
                  let oStore = yield cadesplugin.CreateObjectAsync(
                    "CAdESCOM.Store"
                  );
                  yield oStore.Open(
                    CAPICOM_CURRENT_USER_STORE,
                    CAPICOM_MY_STORE,
                    CAPICOM_STORE_OPEN_MAXIMUM_ALLOWED
                  );

                  let oStoreCerts = yield oStore.Certificates;
                  let oCertificates = yield oStoreCerts.Find(
                    CAPICOM_CERTIFICATE_FIND_SUBJECT_NAME,
                    sCertName
                  );
                  let certsCount = yield oCertificates.Count;
                  if (certsCount === 0) {
                    alert("Сертификаты не найдены: " + sCertName);
                    return;
                  }

                  let oCertificate = yield oCertificates.Item(1);

                  // атрибуты

                  let oSigningTimeAttr = yield cadesplugin.CreateObjectAsync(
                    "CADESCOM.CPAttribute"
                  );
                  yield oSigningTimeAttr.propset_Name(
                    CAPICOM_AUTHENTICATED_ATTRIBUTE_SIGNING_TIME
                  );
                  let oTimeNow = new Date();
                  yield oSigningTimeAttr.propset_Value(ConvertDate(oTimeNow));

                  //дальше

                  let oSigner = yield cadesplugin.CreateObjectAsync(
                    "CAdESCOM.CPSigner"
                  );
                  yield oSigner.propset_Certificate(oCertificate);
                  yield oSigner.propset_CheckCertificate(true);

                  // атрибуты
                  let oAuthAttrs = yield oSigner.AuthenticatedAttributes2;
                  yield oAuthAttrs.Add(oSigningTimeAttr);

                  //дальше

                  let oSignedData = yield cadesplugin.CreateObjectAsync(
                    "CAdESCOM.CadesSignedData"
                  );
                  yield oSignedData.propset_ContentEncoding(
                    CADESCOM_BASE64_TO_BINARY
                  );
                  yield oSignedData.propset_Content(sBase64Data);

                  try {
                    var sSignedMessage = yield oSignedData.SignCades(
                      oSigner,
                      CADESCOM_CADES_BES,
                      true
                    );
                  } catch (err) {
                    alert(
                      "Ошибка при создании подписи. Код ошибки: " +
                        cadesplugin.getLastError(err)
                    );
                    return;
                  }

                  yield oStore.Close();

                  getFileFromZip().then((file) => {
                    formSubmit(event, sSignedMessage, file);
                  });

                  // проверка
                  let oSignedData2 = yield cadesplugin.CreateObjectAsync(
                    "CAdESCOM.CadesSignedData"
                  );
                  try {
                    yield oSignedData2.propset_ContentEncoding(
                      CADESCOM_BASE64_TO_BINARY
                    );
                    yield oSignedData2.propset_Content(sBase64Data);
                    yield oSignedData2.VerifyCades(
                      sSignedMessage,
                      CADESCOM_CADES_BES,
                      true
                    );
                  } catch (err) {
                    alert("Ошибка проверки подписи, попробуйте еще раз");
                    console.log(cadesplugin.getLastError(err));
                    return;
                  }
                });
              };
            });
          });
        }
      });
    });
  });
});
