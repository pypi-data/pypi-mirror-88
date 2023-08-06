define([
    'require'
    , 'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
], function (requirejs, $, vpCommon) {

    /*
        // 사용자 정의 dom을 생성하는 함수
        MakeDom함수 예제
        1. MakeDom("div", { innerHTML:"안녕하세요"});
                -> <div>​안녕하세요</div>​
            
        2. MakeDom("div", { classList:"white",
                            innerHTML:"안녕하세요" });
                -> <div class=​"white">안녕하세요​</div>​

        3. MakeDom("div", { onclick:function() {console.log(1);} ,
                            innerHTML:"안녕하세요",
                            classList:"white"  
                            });
        -> <div class=​"white" onclick>​안녕하세요</div>​
    */
   var makeDom = function(tagSelector, attribute = {}) {
        const dom = Object.entries(attribute).reduce((element, value) => {
            typeof element[value[0]] === 'function' 
                            ? element[value[0]](value[1]) 
                            : (element[value[0]] = value[1]);
            return element;
        }, document.createElement(tagSelector));

        return dom;
    }

    // fileNavigation 등의 hotkey 제어 input text 인 경우 포커스를 가지면 핫키 막고 잃으면 핫키 허용
    var controlToggleInput = function() {
        $(`#vp_fileNavigation`).on("focus", ".FileNavigationPage-container input[type='text']", function() {
            Jupyter.notebook.keyboard_manager.disable();
        });
        $(`#vp_fileNavigation`).on("blur", ".FileNavigationPage-container input[type='text']", function() {
            Jupyter.notebook.keyboard_manager.enable();
        });
    }
    
    // var closeParamArrayEditor = function(numpyPageRenderThis, tagSelector, stateParamName, arrayEditorType) {
    //     $('#vp_fileNavigation').addClass("hide");
    //     $('#vp_fileNavigation').removeClass("show");
    //     $('#vp_fileNavigation').remove();
        
    //     vpCommon.removeHeadScript("fileNavigation");

    //     switch(arrayEditorType){
    //         case 0: {
    //             numpyPageRenderThis.renderParamOneArrayEditor(tagSelector, stateParamName);
    //             vpCommon.removeHeadScript("oneArrayEditor");
    //             break;
    //         }
    //         case 1: {
    //             numpyPageRenderThis.renderParamTwoArrayEditor(tagSelector, stateParamName);
    //             vpCommon.removeHeadScript("twoArrayEditor");
    //             break;
    //         }
    //         case 2: {
    //             numpyPageRenderThis.renderParamThreeArrayEditor(tagSelector, stateParamName);
    //             vpCommon.removeHeadScript("threeArrayEditor");
    //             break;
    //         }
    //         default: {
    //             break;
    //         }
    //     }
    // }
    var importVisualPythonData = function(file, callback) {
        var rawFile = new XMLHttpRequest();
        rawFile.overrideMimeType("application/json");
        rawFile.open("GET", file, true);
        rawFile.onreadystatechange = function() {
            if (rawFile.readyState === 4 && rawFile.status == "200") {
                callback(rawFile.responseText);
            }
        }
        rawFile.send(null);
    }
    
    // var closeComponent = () => {
    //     $('#vp_fileNavigation').addClass("hide");
    //     $('#vp_fileNavigation').removeClass("show");
    //     $('#vp_fileNavigation').remove();
    //     vpCommon.removeHeadScript("fileNavigation");
    // }

    return {
        makeDom
        , controlToggleInput
        // , closeParamArrayEditor
        , importVisualPythonData
        // , closeComponent
    }
});
