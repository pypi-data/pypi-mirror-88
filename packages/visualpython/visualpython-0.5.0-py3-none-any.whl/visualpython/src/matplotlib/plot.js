define([
    'require'
    , 'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    , 'nbextensions/visualpython/src/common/vpFuncJS'
    , 'nbextensions/visualpython/src/container/vpContainer'
    , 'nbextensions/visualpython/src/pandas/common/pandasGenerator'
    , 'nbextensions/visualpython/src/pandas/fileNavigation/index'
], function (requirejs, $, vpCommon, vpConst, sb, vpFuncJS, vpContainer, pdGen, fileNavigation) {
    // 옵션 속성
    const funcOptProp = {
        stepCount : 1
        , funcName : "Create chart"
        , funcID : "mp_plot"  // TODO: ID 규칙 생성 필요
    }

    //////////////// FIXME: move to constants file: Data Types constant ///////////////////////

    var _DATA_TYPES_OF_INDEX = [
        // Index 하위 유형
        'RangeIndex', 'CategoricalIndex', 'MultiIndex', 'IntervalIndex', 'DatetimeIndex', 'TimedeltaIndex', 'PeriodIndex', 'Int64Index', 'UInt64Index', 'Float64Index'
    ]

    var _DATA_TYPES_OF_GROUPBY = [
        // GroupBy 하위 유형
        'DataFrameGroupBy', 'SeriesGroupBy'
    ]

    var _SEARCHABLE_DATA_TYPES = [
        // pandas 객체
        'DataFrame', 'Series', 'Index', 'Period', 'GroupBy', 'Timestamp'
        , ..._DATA_TYPES_OF_INDEX
        , ..._DATA_TYPES_OF_GROUPBY
        // Plot 관련 유형
        //, 'Figure', 'AxesSubplot'
        // Numpy
        //, 'ndarray'
        // Python 변수
        //, 'str', 'int', 'float', 'bool', 'dict', 'list', 'tuple'
    ];

    /**
     * html load 콜백. 고유 id 생성하여 부과하며 js 객체 클래스 생성하여 컨테이너로 전달
     * @param {function} callback 호출자(컨테이너) 의 콜백함수
     */
    var optionLoadCallback = function(callback, meta) {
        // document.getElementsByTagName("head")[0].appendChild(link);
        // 컨테이너에서 전달된 callback 함수가 존재하면 실행.
        if (typeof(callback) === 'function') {
            var uuid = vpCommon.getUUID();
            // 최대 10회 중복되지 않도록 체크
            for (var idx = 0; idx < 10; idx++) {
                // 이미 사용중인 uuid 인 경우 다시 생성
                if ($(vpConst.VP_CONTAINER_ID).find("." + uuid).length > 0) {
                    uuid = vpCommon.getUUID();
                }
            }
            $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.OPTION_GREEN_ROOM))).find(vpCommon.formatString(".{0}", vpConst.API_OPTION_PAGE)).addClass(uuid);

            // 옵션 객체 생성
            var mpPackage = new MatplotPackage(uuid);
            mpPackage.metadata = meta;

            // 옵션 속성 할당.
            mpPackage.setOptionProp(funcOptProp);
            // html 설정.
            mpPackage.initHtml();
            callback(mpPackage);  // 공통 객체를 callback 인자로 전달
        }
    }
    
    /**
     * html 로드. 
     * @param {function} callback 호출자(컨테이너) 의 콜백함수
     */
    var initOption = function(callback, meta) {
        vpCommon.loadHtml(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.OPTION_GREEN_ROOM)), "matplotlib/plot.html", optionLoadCallback, callback, meta);
    }

    /**
     * 본 옵션 처리 위한 클래스
     * @param {String} uuid 고유 id
     */
    var MatplotPackage = function(uuid) {
        this.uuid = uuid;           // Load html 영역의 uuid.

        this.setDefaultVariables();
    }



    /**
     * vpFuncJS 에서 상속
     */
    MatplotPackage.prototype = Object.create(vpFuncJS.VpFuncJS.prototype);

    /**
     * 유효성 검사
     * @returns 유효성 검사 결과. 적합시 true
     */
    MatplotPackage.prototype.optionValidation = function() {
        return true;

        // 부모 클래스 유효성 검사 호출.
        // vpFuncJS.VpFuncJS.prototype.optionValidation.apply(this);
    }


    /**
     * html 내부 binding 처리
     */
    MatplotPackage.prototype.initHtml = function() {
        var that = this;

        this.loadCss(Jupyter.notebook.base_url + vpConst.BASE_PATH + vpConst.STYLE_PATH + "pandas/commonPandas.css");
        this.loadCss(Jupyter.notebook.base_url + vpConst.BASE_PATH + vpConst.STYLE_PATH + "matplotlib/plot.css");

        this.showFunctionTitle();
        
        // 차트 서브플롯 페이지 구성
        this.bindSubplotOption1();
        this.bindCmapSelector();

        this.bindSubplotOption2();

        // variable selector
        this.bindVariableSelector();

        // close variable selector
        $('body').on('click', function(evt) {
            // plot select box 닫기
            if (evt.target.id != vpConst.VP_PLOT_SELECT_BOX_ID
                && !$(evt.target).hasClass('vp-select-data')) {
                if ($(evt.target).parents('#' + vpConst.VP_PLOT_SELECT_BOX_ID).length <= 0) {
                    $(that.wrapSelector('#' + vpConst.VP_PLOT_SELECT_BOX_ID)).hide();

                    // init boxes
                    $(that.wrapSelector('#vp_varDetailColList')).html('');
                    $(that.wrapSelector('#vp_varDetailDtype')).val('');
                    $(that.wrapSelector('#vp_varDetailArray')).html('');
                }
            }
        }); 
    }

    /**
     * 선택한 패키지명 입력
     */
    MatplotPackage.prototype.showFunctionTitle = function() {
        $(this.wrapSelector('.vp_functionName')).text(funcOptProp.funcName);
    }

    /**
     * 서브플롯 옵션 페이지 구성
     */
    MatplotPackage.prototype.bindSubplotOption1 = function() {
        var that = this;

        // 차트 유형 선택지 구성
        this.bindKindSelector();

        // 색상 사용여부
        $(this.wrapSelector('#useColor')).change(function() {
            var checked = $(this).prop('checked');
            if (checked == true) {
                // 색상 선택 가능하게
                $(that.wrapSelector('#color')).removeAttr('disabled');
            } else {
                $(that.wrapSelector('#color')).attr('disabled', 'true');
            }
        })

        // 마커 이미지 표시 (또는 hover에 표시)
        var optionTagList = $(this.wrapSelector('#markerSelector option'));
        // [0] 직접입력 제외
        for (var i = 1; i < optionTagList.length; i++) {
            // 이미지 파일명
            var imgFile = $(optionTagList[i]).data('img');
            // 이미지 url 바인딩
            var url = Jupyter.notebook.base_url + vpConst.BASE_PATH + vpConst.RESOURCE_PATH + 'matplotlib/' + imgFile;
            $(optionTagList[i]).attr({
                'data-img': url
            });
        }

        // 마커 : 직접입력 선택 시 input 태그 활성화
        $(this.wrapSelector('#markerSelector')).change(function() {
            var selected = $(this).val();
            if (selected == "marker") {
                $(this).parent().find('#marker').show();
                $(this).parent().find('#marker').val('');
            } else {
                $(this).parent().find('#marker').hide();
                $(this).parent().find('#marker').val(selected);
            }
        });
    }

    MatplotPackage.prototype.bindSubplotOption2 = function() {
        var that = this;
        // 파일 네비게이션 오픈
        $(this.wrapSelector('#vp_openFileNavigationBtn')).click(async function() {
            
            var loadURLstyle = Jupyter.notebook.base_url + vpConst.BASE_PATH + vpConst.STYLE_PATH;
            var loadURLhtml = Jupyter.notebook.base_url + vpConst.BASE_PATH + vpConst.SOURCE_PATH + "component/fileNavigation/index.html";
            
            that.loadCss( loadURLstyle + "component/fileNavigation.css");
    
            await $(`<div id="vp_fileNavigation"></div>`)
                    .load(loadURLhtml, () => {

                        $('#vp_fileNavigation').removeClass("hide");
                        $('#vp_fileNavigation').addClass("show");

                        var { vp_init
                              , vp_bindEventFunctions } = fileNavigation;
                    
                        fileNavigation.vp_init(that, "SAVE_FILE");
                        // fileNavigation.vp_init(that.getStateAll());
                        fileNavigation.vp_bindEventFunctions();
                    })
                    .appendTo("#site");
        });
    }

    /**
     * 차트 유형 선택지 구현
     */
    MatplotPackage.prototype.bindKindSelector = function() {
        // 차트유형 selector 동적 구성
        var selector = $(this.wrapSelector('#kind'));
        var that = this;
        this.plotKind.forEach(kind => {
            var option = document.createElement('option');
            $(option).attr({
                id: kind,
                name: 'kind',
                value: kind
            });
            var span = document.createElement('span');
            $(span).attr({
                // class="vp-multilang" data-caption-id="imshow"
                class: 'vp-multilang',
                'data-caption-id':kind
            });
            span.append(document.createTextNode(that.plotKindLang[kind]))
            option.appendChild(span);
            selector.append(option);
        });

        // 메타데이터로 차트유형 선택
        var plotType = 'plot';
        if (this.metadata != undefined && this.metadata.options != undefined) {
            plotType = this.metadata.options.filter(o => o.id == 'kind')[0].value;
        }

        // 차트 선택
        $(selector).val(plotType);
        $(this.wrapSelector(`#vp_plotKind .vp-plot-item[data-kind="${plotType}"]`)).addClass('selected');
        
        // 기존 유형 선택하는 select 태그 안보이게
        $(selector).hide();

        // 차트유형 선택지에 맞게 옵션 표시
        $(this.wrapSelector('#vp_plotKind .vp-plot-item')).click(function() {
            // 선택한 플롯 유형 박스 표시
            $(this).parent().find('.vp-plot-item').removeClass('selected');
            $(this).addClass('selected');

            // select 태그 강제 선택
            var kind = $(this).data('kind');
            $(selector).val(kind).prop('selected', true);

            var package = { ...that.plotPackage[kind] };          
            if (package == undefined) package = that.plotPackage['plot'];

            // 모두 숨기기 (단, 대상 변수 입력란과 차트 유형 선택지 제외)
            $(that.wrapSelector('#vp_plotSetting table tr:gt(1):not(:last)')).hide();

            // 해당 옵션에 있는 선택지만 보이게 처리
            package.input && package.input.forEach(obj => {
                $(that.wrapSelector('#' + obj.name)).closest('tr').show();

                var label = obj.label;
                if (label != undefined) {
                    if (obj.required != false) {
                        label = "* " + obj.label;
                    }
                    $(that.wrapSelector("label[for='" + obj.name + "']")).text(label);
                }
            });
            package.variable && package.variable.forEach(obj => {
                $(that.wrapSelector('#' + obj.name)).closest('tr').show();
            });

            package.input = package.input.concat(that.addOption);
            this.package = package;
        });

        // 플롯 차트 옵션으로 초기화
        var plotPackage = { ...this.plotPackage[plotType] };
        // 모두 숨기기 (단, 대상 변수 입력란과 차트 유형 선택지 제외)
        $(this.wrapSelector('#vp_plotSetting table tr:gt(1):not(:last)')).hide();

        // 해당 옵션에 있는 선택지만 보이게 처리
        plotPackage.input && plotPackage.input.forEach(obj => {
            $(this.wrapSelector('#' + obj.name)).closest('tr').show();
            var label = obj.label;
            if (label != undefined) {
                if (obj.required != false) {
                    label = "* " + obj.label;
                }
                $(this.wrapSelector("label[for='" + obj.name + "']")).text(label);
            }
        });
        plotPackage.variable && plotPackage.variable.forEach(obj => {
            $(this.wrapSelector('#' + obj.name)).closest('tr').show();
        });

        plotPackage.input = plotPackage.input.concat(this.addOption);
        this.package = plotPackage;
    }

    /**
     * 색상 스타일 선택지 구현
     */
    MatplotPackage.prototype.bindCmapSelector = function() {
        // 기존 cmap 선택하는 select 태그 안보이게
        var cmapSelector = this.wrapSelector('#cmap');
        $(cmapSelector).hide();

        // cmap 데이터로 cmap selector 동적 구성
        this.cmap.forEach(ctype => {
            var option = document.createElement('option');
            $(option).attr({
                'name': 'cmap',
                'value': ctype
            });
            $(option).text(ctype == ''?'none':ctype);
            $(cmapSelector).append(option);
        });

        // cmap 데이터로 팔레트 div 동적 구성
        this.cmap.forEach(ctype => {
            var divColor = document.createElement('div');
            $(divColor).attr({
                'class': 'vp-plot-cmap-item',
                'data-cmap': ctype,
                'data-url': 'pandas/cmap/' + ctype + '.JPG',
                'title': ctype
            });
            $(divColor).text(ctype == ''?'none':ctype);
            
            // 이미지 url 바인딩
            var url = Jupyter.notebook.base_url + vpConst.BASE_PATH + vpConst.RESOURCE_PATH + 'pandas/cmap/' + ctype + '.JPG';
            $(divColor).css({
                'background-image' : 'url(' + url + ')'
            })

            var selectedCmap = this.wrapSelector('#vp_selectedCmap');

            // 선택 이벤트 등록
            $(divColor).click(function() {
                if (!$(this).hasClass('selected')) {
                    $(this).parent().find('.vp-plot-cmap-item.selected').removeClass('selected');
                    $(this).addClass('selected');
                    // 선택된 cmap 이름 표시
                    $(selectedCmap).text(ctype == ''?'none':ctype);
                    // 선택된 cmap data-caption-id 변경
                    $(selectedCmap).attr('data-caption-id', ctype);
                    // select 태그 강제 선택
                    $(cmapSelector).val(ctype).prop('selected', true);
                }
            });
            $(this.wrapSelector('#vp_plotCmapSelector')).append(divColor);
        });

        // 선택 이벤트
        $(this.wrapSelector('.vp-plot-cmap-wrapper')).click(function() {
            $(this).toggleClass('open');
        });
    }

    MatplotPackage.prototype.bindVariableSelector = function() {
        var that = this;
        // view button click - view little popup to show variable & details
        $(this.wrapSelector('.vp-select-data')).click(function(event) {
            var axes = $(this).data('axes');
            
            if($(that.wrapSelector('#vp_varViewBox')).is(":hidden")) {
                // refresh variables
                that.refreshVariables(function(varList) {
                    // set position
                    var boxSize = { width: 280, height: 260 };
                    var boxPosition = { position: 'fixed', left: event.pageX - 20, top: event.pageY + 20 };
                    if (event.pageX + boxSize.width > window.innerWidth) {
                        boxPosition.left = event.pageX - boxSize.width;
                    }
                    if (event.pageY + boxSize.height > window.innerHeight) {
                        boxPosition.top = event.pageY - boxSize.height - 20;
                    }
                    $('#vp_varViewBox').css({
                        ...boxPosition
                    });
    
                    // set axes and prev code
                    $(that.wrapSelector('#vp_varViewBox')).attr({
                        'data-axes': axes
                    });
                    $(that.wrapSelector('#vp_varSelectCode')).val($(that.wrapSelector('#' + axes)).val());
    
                    // show popup area
                    $(that.wrapSelector('#vp_varViewBox')).show();
                });

            } else {
                // hide popup area
                $(that.wrapSelector('#vp_varViewBox')).hide();

                // init boxes
                $(that.wrapSelector('#vp_varDetailColList')).html('');
                $(that.wrapSelector('#vp_varDetailDtype')).val('');
                $(that.wrapSelector('#vp_varDetailArray')).html('');
            }
        });
        // view close button click
        $(this.wrapSelector('.vp-close-view')).click(function(event) {
            // hide view
            // show/hide popup area
            $(that.wrapSelector('#vp_varViewBox')).toggle();
        });

        // view object selection
        $(document).on('click', this.wrapSelector('.vp-var-view-item'), function(event) {
            // set selection style
            // TODO: attach .selected
            $(that.wrapSelector('.vp-var-view-item')).removeClass('selected');
            $(this).addClass('selected');

            var varName = $(this).find('td:first').text();
            var varType = $(this).find('td:last').text();

            // set code
            $(that.wrapSelector('#vp_varSelectCode')).val(varName);

            // dataframe : columns, dtypes, array
            // series : array
            // use json.dumps to make python dict/list to become parsable with javascript JSON
            var code = new sb.StringBuilder();
            code.appendLine('import json');
            if (varType == 'DataFrame') {
                code.append(`print(json.dumps([ { "colName": c, "dtype": str(${varName}[c].dtype), "array": str(${varName}[c].array) } for c in list(${varName}.columns) ]))`);
            } else if (varType == 'Series') {
                code.append(`print(json.dumps({"dtype": str(${varName}.dtype), "array": str(${varName}.array) }))`);
            }

            // get result and show on detail box
            that.kernelExecute(code.toString(), function(result) {
                var varResult = JSON.parse(result);

                $(that.wrapSelector('#vp_varDetailColList')).html('');
                
                var methodList = [];
                // DataFrame / Series Detail
                if (varType == 'DataFrame') {
                    if (varResult.length > 0) {
                        varResult.forEach(v => {
                            // var option = $(`<option value="${v.colName}" data-dtype="${v.dtype}" data-array="${v.array}">${v.colName}</option>`)
                            var option = $(`<div class="vp-column-select-item" 
                                            data-dtype="${v.dtype}" data-array="${v.array}" data-col="${v.colName}" title="${v.array}">
                                                ${v.colName}</div>`);
                            $(that.wrapSelector('#vp_varDetailColList')).append(option);
                        });

                        // $(that.wrapSelector('#vp_varDetailDtype')).val(varResult[0].dtype);

                        // var array = varResult[0].array.replaceAll('/n', '\n');
                        // $(that.wrapSelector('#vp_varDetailArray')).text(array);
                    }

                    // method for object
                    methodList = [
                        { method: 'index', label: 'index' },
                        { method: 'columns', label: 'columns' },
                        { method: 'values', label: 'values' }
                    ]
                    var methodArrayCode = new sb.StringBuilder();
                    methodList.forEach(m => {
                        methodArrayCode.appendFormat('<div class="{0}" data-method="{1}">{2}</div>', 'vp-method-select-item', m.method, m.label);
                    });
                    $(that.wrapSelector('#vp_varDetailArray')).html(methodArrayCode.toString());

                    // show columns
                    // $(that.wrapSelector('#vp_varDetailColList')).closest('tr').show();
                    $(that.wrapSelector('#vp_varDetailColList')).attr({'disabled': false});
                } else if (varType == 'Series') {
                    $(that.wrapSelector('#vp_varDetailDtype')).val(varResult.dtype);
                    var array = varResult.array.replaceAll('/n', '\n');
                    // $(that.wrapSelector('#vp_varDetailArray')).text(array);

                    // method for object
                    methodList = [
                        { method: 'index', label: 'index' },
                        { method: 'values', label: 'values' }
                    ]
                    var methodArrayCode = new sb.StringBuilder();
                    methodList.forEach(m => {
                        methodArrayCode.appendFormat('<div class="{0}" data-method="{1}">{2}</div>', 'vp-method-select-item', m.method, m.label);
                    });
                    $(that.wrapSelector('#vp_varDetailArray')).html(methodArrayCode.toString());

                    // disable columns
                    $(that.wrapSelector('#vp_varDetailColList')).attr({'disabled': true});
                }

            });
        });

        // view column selection
        $(document).on('click', this.wrapSelector('#vp_varDetailColList .vp-column-select-item'), function() {
            var dtype = $(this).data('dtype');
            var array = $(this).data('array');

            var kind = $(that.wrapSelector('#kind')).val();
            var axes = $(that.wrapSelector('#vp_varViewBox')).attr('data-axes');

            $(this).toggleClass('selected');

            // if ((kind == 'plot' && axes == 'y')
            //     || (kind == 'bar' && axes == 'y')) {
            // allow multi select
            var methodArrayCode = new sb.StringBuilder();
            var methodList;
            // 선택된 항목들 중 categorical variable 존재하면 categorical로 분류
            var hasObject = false;
            var selectedColumnList = $(that.wrapSelector('#vp_varDetailColList .vp-column-select-item.selected'));
            if (selectedColumnList.length > 0) {
                selectedColumnList.each((i, tag) => {
                    var tagDtype = $(tag).data('dtype');
                    if (tagDtype == 'object') {
                        hasObject = true;
                    }
                });
            }
            if (dtype != undefined) {
                if (hasObject == true) {
                    // categorical variable
                    methodList = that.methodList.categorical;
                } else {
                    // numeric variable
                    methodList = that.methodList.numerical;
                }
                methodList = [ 
                    { method: 'index', label: 'index' },
                    { method: 'columns', label: 'columns' },
                    { method: 'values', label: 'values' },
                    ...methodList
                ]
                methodList.forEach(m => {
                    methodArrayCode.appendFormat('<div class="{0}" data-method="{1}">{2}</div>', 'vp-method-select-item', m.method, m.label);
                });
            }
            $(that.wrapSelector('#vp_varDetailArray')).html(methodArrayCode.toString());

            
            // } else {
            //     // select only one at a time
            //     var methodArrayCode = new sb.StringBuilder();
            //     if (dtype != undefined) {
            //         methodArrayCode.appendFormat('<div class="{0}" data-method="{1}">{2}</div>', 'vp-method-select-item', 'index', 'index');
            //         methodArrayCode.appendFormat('<div class="{0}" data-method="{1}">{2}</div>', 'vp-method-select-item', 'values', 'values');
            //     }
            //     $(that.wrapSelector('#vp_varDetailArray')).html(methodArrayCode.toString());
    
            //     var nowState = $(this).hasClass('selected');
            //     $(that.wrapSelector('#vp_varDetailColList .vp-column-select-item')).removeClass('selected');
            //     if (nowState == false) {
            //         $(this).addClass('selected');
            //     }
            // }

            // set code
            var code = that.getSelectCode();
            $(that.wrapSelector('#vp_varSelectCode')).val(code);
        });

        // view method selection
        $(document).on('click', this.wrapSelector('#vp_varDetailArray .vp-method-select-item'), function() {
            var method = $(this).data('method');
            var nowState = $(this).hasClass('selected');

            $(that.wrapSelector('#vp_varDetailArray .vp-method-select-item')).removeClass('selected');
            if (nowState == false) {
                $(this).addClass('selected');
            }

            // set code
            var code = that.getSelectCode();
            $(that.wrapSelector('#vp_varSelectCode')).val(code);
        });

        // enter variables button 
        $(this.wrapSelector('#vp_varSelectBtn')).click(function() {
            var axes = $(that.wrapSelector('#vp_varViewBox')).attr('data-axes');
            var code = $(that.wrapSelector('#vp_varSelectCode')).val();
            
            // set code
            $(that.wrapSelector('#' + axes)).val(code);

            // hide view box
            $(that.wrapSelector('#vp_varViewBox')).hide();

            // init boxes
            $(that.wrapSelector('#vp_varDetailColList')).html('');
            $(that.wrapSelector('#vp_varDetailDtype')).val('');
            $(that.wrapSelector('#vp_varDetailArray')).html('');
        });
    }

    /**
     * get selected object + details as code
     */
    MatplotPackage.prototype.getSelectCode = function() {
        var code = new sb.StringBuilder();

        // variable
        var variable = $(this.wrapSelector('.vp-var-view-item.selected td:first')).text();
        if (variable == undefined) return "";
        
        code.append(variable);

        // columns
        var columnsTag = $(this.wrapSelector('.vp-column-select-item.selected'));
        if (columnsTag.length > 0) {
            if (columnsTag.length == 1) {
                code.append('[');
            } else {
                code.append('[[');
            }
            columnsTag.each((i, tag) => {
                if (i > 0) {
                    code.append(', ');
                }
                var colName = $(tag).data('col');
                code.append(convertToStr(colName));
            });
            if (columnsTag.length == 1) {
                code.append(']');
            } else {
                code.append(']]');
            }
        }
        
        // method
        var method = $(this.wrapSelector('.vp-method-select-item.selected')).data('method');
        if (method != undefined) {
            code.appendFormat('.{0}', method);
        }

        return code.toString();
    }

    var convertToStr = function(code) {
        if (!$.isNumeric(code)) {
            code = `'${code}'`;
        }
        return code;
    }

    /**
     * refresh variable list to select box
     */
    MatplotPackage.prototype.refreshVariables = function(callback = undefined) {
        var that = this;

        // 조회가능한 변수 data type 정의 FIXME: 조회 필요한 변수 유형 추가
        var types = _SEARCHABLE_DATA_TYPES;

        // View 초기화
        var viewList = $(this.wrapSelector('#vp_varViewList tbody'));
        $(viewList).html('');

        pdGen.vp_searchVarList(types, function(result) {
            var jsonVars = result.replace(/'/gi, `"`);
            var varList = JSON.parse(jsonVars);

            var hasVariable = false;
            // 변수목록 추가
            varList.forEach(varObj => {
                if (types.includes(varObj.varType) && varObj.varName[0] !== '_') {
                    var varAttr = {
                        'data-var-name': varObj.varName,
                        'data-var-type': varObj.varType,
                        'value': varObj.varName
                    };

                    // View Table에 추가
                    var tagRow = $(`<tr class="vp-var-view-item"><td>${varObj.varName}</td><td>${varObj.varType}</td></tr>`);
                    $(viewList).append(tagRow);
                }
            });
            
            // callback
            if (callback != undefined) {
                callback(varList);
            }

        });
    }

    /**
     * 간단 코드 변환기
     * @param {string} code 코드 
     * @param {Array} input 변수 목록
     */
    MatplotPackage.prototype.simpleCodeGenerator = function(code, input, variable=[]) {
        var hasValue = false;
        input && input.forEach(obj => {
            var val = pdGen.vp_getTagValue(this.uuid, obj);
            if (val != '' && val != 'plt') {
                hasValue = true;
                if (obj.type == 'text') {
                    val = "'"+val+"'";
                } else if (obj.type == 'list') {
                    val = '['+val+']';
                }
            }
            code = code.split('${' + obj.name + '}').join(val);
        });
        var opt_params = '';
        variable && variable.forEach(obj => {
            var val = pdGen.vp_getTagValue(this.uuid, obj);
            if (val != '') {
                hasValue = true;
                if (obj.type == 'text') {
                    val = "'"+val+"'";
                } else if (obj.type == 'list') {
                    val = '['+val+']';
                }
                opt_params += ', ' + obj.key + '=' + val;
            }
        });
        code = code.split('${v}').join(opt_params);

        // () 함수 파라미터 공간에 input 없을 경우 (, ${v}) 와 같은 형태로 출력되는 것 방지
        code = code.split('(, ').join('(');

        if (!hasValue) {
            return '';
        }

        return code;
    }

    /**
     * 코드 생성
     * @param {boolean} exec 실행여부
     */
    MatplotPackage.prototype.generateCode = function(addCell, exec) {
        if (!this.optionValidation()) return;

        try {
            var sbCode = new sb.StringBuilder();

            // add prefix code
            var prefixCode = $(this.wrapSelector('#vp_prefixBox textarea')).val();
            if (prefixCode.length > 0) {
                sbCode.appendLine(prefixCode);
            }

            // 대상 변수가 입력되어 있지 않으면 plot(plt) 포커스에 차트 그리기
            // var i0Input = $(this.wrapSelector('#i0_input')).val();
            // var usePlotFunction = (i0Input == ''); // 대상 변수로 plt 를 사용할지 여부
            var i0Input = 'plt'; // FIXME: matplotlib.pyplot setting value

            // 패키지 복사
            var kind = $(this.wrapSelector('#kind')).val();
            var package = this.plotPackage[kind];
            // 원하는 패키지가 없으면 기본 플롯 옵션 불러오기
            if (package == undefined) {
                package = this.plotPackage['plot'];
            }
            package = JSON.parse(JSON.stringify(package));

            // 색상 사용 안하면 코드에 표시되지 않도록
            if ($(this.wrapSelector('#useColor')).prop('checked') != true) {
                var idx = package.variable.findIndex(function(item) {return item.name === 'color'});
                if (idx > -1) {
                    package.variable.splice(idx, 1);
                }
            }

            // 사용자 옵션 설정값 가져오기
            var userOption = new sb.StringBuilder();
            var userOptValue = $(this.wrapSelector('#vp_userOption')).val();
            if (userOptValue != '') {
                userOption.appendFormat(', {0}', userOptValue);
            }

            // 플롯 구성 코드 생성
            var plotCode = pdGen.vp_codeGenerator(this.uuid, package, userOption.toString());
            if (plotCode == null) return "BREAK_RUN"; // 코드 생성 중 오류 발생
            sbCode.append(plotCode);

            // 꼬리 코드 입력
            if (package.tailCode != undefined) {
                sbCode.append('\n' + package.tailCode.split('${i0}').join(i0Input));
            }

            // 추가 구성 코드 생성
            for (var i = 0; i < this.optPackList.length; i++) {
                var opt = this.optPackList[i];
                // 주요 값이 없으면 패스
                if ($(this.wrapSelector('#'+opt)).val() == '') {
                    continue;
                }

                var pack = this.optionalPackage[opt];
                // plt 함수 사용
                var code = this.simpleCodeGenerator(pack.code2, pack.input, pack.variable);
                if (code != '') {
                    sbCode.append('\n' + code);
                }
            }

            // plt.show()
            sbCode.appendLine();
            sbCode.append('plt.show()');

            // add postfix code
            var postfix = $(this.wrapSelector('#vp_postfixBox textarea')).val();
            if (postfix.length > 0) {
                sbCode.appendLine('');
                sbCode.append(postfix);
            }

            // 코드 추가 및 실행
            if (addCell) {
                this.cellExecute(sbCode.toString(), exec);
            }
        } catch (exmsg) {
            // 에러 표시
            vpCommon.renderAlertModal(exmsg);
            return "BREAK_RUN"; // 코드 생성 중 오류 발생
        }

        return sbCode.toString();
    }
    
    /**
     * set default variables on construct
     */
    MatplotPackage.prototype.setDefaultVariables = function() {
        // file navigation : state 데이터 목록
        this.state = {
            paramData:{
                encoding: "utf-8" // 인코딩
                , delimiter: ","  // 구분자
            },
            returnVariable:"",    // 반환값
            isReturnVariable: false,
            fileExtension: "png" // 확장자
        };
        this.fileResultState = {
            pathInputId : this.wrapSelector('#savefigpath'),
            fileInputId : this.wrapSelector('#fileName')
        };

        this.plotPackage = {
            'plot': {
                code: '${i0}.${kind}(${x}, ${y}${v}${etc})',
                input: [
                    {
                        name: 'i0',
                        label: 'Axes Variable',
                        type: 'int',
                        required: false
                    },
                    {
                        name: 'kind',
                        type: 'var',
                        label: 'chart type'
                    },
                    {
                        name: 'x',
                        type: 'var',
                        label: 'x data',
                        required: false
                    },
                    {
                        name: 'y',
                        type: 'var',
                        label: 'y data'
                    }
                ],
                variable: [
                    {
                        name: 'label',
                        type: 'text'
                    },
                    {
                        name: 'color', 
                        type: 'text',
                        default: '#000000'
                    },
                    {
                        name: 'marker',
                        type: 'text'
                    },
                    {
                        name: 'linestyle',
                        type: 'text',
                        component: 'option_select',
                        default: '-'
                    }
                ]
            },
            'bar': {
                code: '${i0}.${kind}(${x}, ${y}${v}${etc})',
                input: [
                    {
                        name: 'i0',
                        label: 'axes variable',
                        type: 'int',
                        required: false
                    },
                    {
                        name: 'kind',
                        type: 'var',
                        label: 'chart type'
                    },
                    {
                        name: 'x',
                        type: 'var',
                        label: 'x'
                    },
                    {
                        name: 'y',
                        type: 'var',
                        label: 'height'
                    }
                ],
                variable: [
                    {
                        name: 'label',
                        type: 'text'
                    },
                    {
                        name: 'color', 
                        type: 'text',
                        default: '#000000'
                    },
                    {
                        name: 'linestyle',
                        type: 'text',
                        component: 'option_select',
                        default: '-'
                    }
                ]
            },
            'barh': {
                code: '${i0}.${kind}(${x}, ${y}${v}${etc})',
                input: [
                    {
                        name: 'i0',
                        label: 'axes variable',
                        type: 'int',
                        required: false
                    },
                    {
                        name: 'kind',
                        type: 'var',
                        label: 'chart type'
                    },
                    {
                        name: 'x',
                        type: 'var',
                        label: 'y'
                    },
                    {
                        name: 'y',
                        type: 'var',
                        label: 'width'
                    }
                ],
                variable: [
                    {
                        name: 'label',
                        type: 'text'
                    },
                    {
                        name: 'color', 
                        type: 'text',
                        default: '#000000'
                    },
                    {
                        name: 'linestyle',
                        type: 'text',
                        component: 'option_select',
                        default: '-'
                    }
                ]
            },
            'hist': {
                code: '${i0}.${kind}(${x}${v}${etc})',
                input: [
                    {
                        name: 'i0',
                        label: 'axes variable',
                        type: 'int',
                        required: false
                    },
                    {
                        name: 'kind',
                        type: 'var',
                        label: 'chart type'
                    },
                    {
                        name: 'x',
                        type: 'var',
                        label: 'data'
                    }
                ],
                variable: [
                    {
                        name: 'bins',
                        type: 'int',
                        required: true,
                        label: 'bins' // TODO: 라벨명
                    },
                    {
                        name: 'label',
                        type: 'text'
                    },
                    {
                        name: 'color', 
                        type: 'text',
                        default: '#000000'
                    },
                    {
                        name: 'linestyle',
                        type: 'text',
                        component: 'option_select',
                        default: '-'
                    }
                ]
            },
            'boxplot': {
                code: '${i0}.${kind}(${x}, ${y}${v}${etc})',
                input: [
                    {
                        name: 'i0',
                        label: 'axes variable',
                        type: 'int',
                        required: false
                    },
                    {
                        name: 'kind',
                        type: 'var',
                        label: 'chart type'
                    },
                    {
                        name: 'x',
                        type: 'var',
                        label: 'x data'
                    },
                    {
                        name: 'y',
                        type: 'var',
                        label: 'y data'
                    }
                ],
                variable: [
                ]
            },
            'stackplot': {
                code: '${i0}.${kind}(${x}, ${y}${v}${etc})',
                input: [
                    {
                        name: 'i0',
                        label: 'axes variable',
                        type: 'int',
                        required: false
                    },
                    {
                        name: 'kind',
                        type: 'var',
                        label: 'chart type'
                    },
                    {
                        name: 'x',
                        type: 'var',
                        label: 'x data'
                    },
                    {
                        name: 'y',
                        type: 'var',
                        label: 'y data'
                    }
                ],
                variable: [
                    {
                        name: 'color', 
                        type: 'text',
                        default: '#000000'
                    },
                    {
                        name: 'linestyle',
                        type: 'text',
                        component: 'option_select',
                        default: '-'
                    }
                ]
            },
            'pie': {
                code: '${i0}.${kind}(${x}${v}${etc})',
                tailCode: "${i0}.axis('equal')",
                input: [
                    {
                        name: 'i0',
                        label: 'axes variable',
                        type: 'int',
                        required: false
                    },
                    {
                        name: 'kind',
                        type: 'var',
                        label: 'chart type'
                    },
                    {
                        name: 'x',
                        type: 'var',
                        label: 'data'
                    }
                ],
                variable: [
                ]
            },
            'scatter': {
                code: '${i0}.${kind}(${x}, ${y}${v}${etc})',
                input: [
                    {
                        name: 'i0',
                        label: 'axes variable',
                        type: 'int',
                        required: false
                    },
                    {
                        name: 'kind',
                        type: 'var',
                        label: 'chart type'
                    },
                    {
                        name: 'x',
                        type: 'var',
                        label: 'x data'
                    },
                    {
                        name: 'y',
                        type: 'var',
                        label: 'y data'
                    }
                ],
                variable: [
                    {
                        name: 'cmap',
                        type: 'text'
                    },
                    {
                        name: 'marker',
                        type: 'text'
                    }
                ]
            },
            'hexbin': {
                code: '${i0}.${kind}(${x}, ${y}${v}${etc})',
                tailCode: '${i0}.colorbar()', // 색상 막대 범례 표시
                input: [
                    {
                        name: 'i0',
                        label: 'axes variable',
                        type: 'int',
                        required: false
                    },
                    {
                        name: 'kind',
                        type: 'var',
                        label: 'chart type'
                    },
                    {
                        name: 'x',
                        type: 'var',
                        label: 'x data'
                    },
                    {
                        name: 'y',
                        type: 'var',
                        label: 'y data'
                    }
                ],
                variable: [
                    {
                        name: 'label',
                        type: 'text'
                    },
                    {
                        name: 'color', 
                        type: 'text',
                        default: '#000000'
                    }
                ]
            },
            'contour': {
                code: '${i0}.${kind}(${x}, ${y}, ${z}${v}${etc})',
                input: [
                    {
                        name: 'i0',
                        label: 'axes variable',
                        type: 'int',
                        required: false
                    },
                    {
                        name: 'kind',
                        type: 'var',
                        label: 'chart type'
                    },
                    {
                        name: 'x',
                        type: 'var',
                        label: 'x data'
                    },
                    {
                        name: 'y',
                        type: 'var',
                        label: 'y data'
                    },
                    {
                        name: 'z',
                        type: 'var',
                        label: 'z data'
                    }
                ],
                variable: [
                    {
                        name: 'cmap',
                        type: 'text'
                    },
                    {
                        name: 'label',
                        type: 'text'
                    }
                ]
            },
            'imshow': {
                code: '${i0}.${kind}(${z}${v}${etc})',
                input: [
                    {
                        name: 'i0',
                        label: 'axes variable',
                        type: 'int',
                        required: false
                    },
                    {
                        name: 'kind',
                        type: 'var',
                        label: 'chart type'
                    },
                    {
                        name: 'z',
                        type: 'var',
                        label: 'z data'
                    }
                ],
                variable: [
                    {
                        name: 'extent', // [xmin, xmax, ymin, ymax]
                        type: 'var'
                    },
                    {
                        name: 'origin',
                        type: 'text'
                    },
                    {
                        name: 'cmap',
                        type: 'text'
                    }
                ]
            },
            'errorbar': {
                code: '${i0}.${kind}(${x}, ${y}${v}${etc})',
                input: [
                    {
                        name: 'i0',
                        label: 'axes variable',
                        type: 'int',
                        required: false
                    },
                    {
                        name: 'kind',
                        type: 'var',
                        label: 'chart type'
                    },
                    {
                        name: 'x',
                        type: 'var',
                        label: 'x data'
                    },
                    {
                        name: 'y',
                        type: 'var',
                        label: 'y data'
                    }
                ],
            }
        };
        
        this.optPackList = ['title', 'xlabel', 'ylabel', 'xlim', 'ylim', 'legend', 'savefig'];
        this.optionalPackage = {
            'title': {
                code: '${i0}.set_title(${title})',
                code2: 'plt.title(${title})',
                input: [
                    {
                        name: 'i0',
                        type: 'var',
                        required: false
                    },
                    {
                        name: 'title',
                        type: 'text',
                        required: false
                    }
                ]
            },
            'xlabel': {
                code: '${i0}.set_xlabel(${xlabel})',
                code2: 'plt.xlabel(${xlabel})',
                input: [
                    {
                        name: 'i0',
                        type: 'var',
                        required: false
                    },
                    {
                        name: 'xlabel',
                        type: 'text',
                        required: false
                    }
                ]
            },
            'ylabel': {
                code: '${i0}.set_ylabel(${ylabel})',
                code2: 'plt.ylabel(${ylabel})',
                input: [
                    {
                        name: 'i0',
                        type: 'var',
                        required: false
                    },
                    {
                        name: 'ylabel',
                        type: 'text',
                        required: false
                    }
                ]
            },
            'xlim': {
                code: '${i0}.set_xlim(${xlim})',
                code2: 'plt.xlim(${xlim})',
                input: [
                    {
                        name: 'i0',
                        type: 'var',
                        required: false
                    },
                    {
                        name: 'xlim',
                        type: 'var',
                        required: false
                    }
                ]
            },
            'ylim': {
                code: '${i0}.set_ylim(${ylim})',
                code2: 'plt.ylim(${ylim})',
                input: [
                    {
                        name: 'i0',
                        type: 'var',
                        required: false
                    },
                    {
                        name: 'ylim',
                        type: 'var',
                        required: false
                    }
                ]
            },
            'legend': {
                code: '${i0}.legend(${v})',
                code2: 'plt.legend(${v})',
                input: [
                    {
                        name: 'i0',
                        type: 'var'
                    }
                ],
                variable: [
                    {
                        key: 'title',
                        name: 'legendTitle',
                        type: 'text'
                    },
                    {
                        key: 'label',
                        name: 'legendLabel',
                        type: 'var'
                    },
                    {
                        key: 'loc',
                        name: 'legendLoc',
                        type: 'text',
                        component: 'option_select',
                        default: 'best'
                    }
                ]
            },
            'savefig': {
                code: "${i0}.savefig('${savefigpath}')",
                code2: "plt.savefig('${savefigpath}')",
                input: [
                    {
                        name: 'i0',
                        type: 'var'
                    },
                    {
                        name: 'savefigpath',
                        type: 'var'
                    }
                ],
                variable: []
            }
        };
        this.addOption = [
            { name: 'vp_userOption', required: false },
            { name: 'title', required: false },
            { name: 'xlabel', required: false },
            { name: 'ylabel', required: false },
            { name: 'xlim', required: false },
            { name: 'ylim', required: false },
            { name: 'legendTitle', required: false },
            { name: 'legendLabel', required: false },
            { name: 'legendLoc', required: false },
            { name: 'savefigpath', required: false }
        ];
        // plot 종류
        this.plotKind = [
            'plot', 'bar', 'barh', 'hist', 'boxplot', 'stackplot',
            'pie', 'scatter', 'hexbin', 'contour', 'imshow', 'errorbar'
        ];
        this.plotKindLang = {
            'plot': '플롯',
            'bar': '바 차트',
            'barh': '가로 바',
            'hist': '히스토그램',
            'boxplot': '박스 플롯',
            'stackplot': '스택 플롯',
            'pie': '파이 차트',
            'scatter': '스캐터 플롯',
            'hexbin': '헥스빈 플롯',
            'contour': '컨투어 플롯',
            'imshow': '이미지 플롯',
            'errorbar': '오차 막대'
        };
        // cmap 종류
        this.cmap = [
            '', 'viridis', 'plasma', 'inferno', 'magma', 'cividis'
            , 'Pastel1', 'Pastel2', 'Paired', 'Accent', 'Dark2', 'Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'tab20b', 'tab20c'
        ];
        this.methodList = {
            'categorical': [
                { label: 'count', method: 'count()' },
                { label: 'unique count', method: 'unique()' }
            ],
            'numerical': [
                { label: 'count', method: 'count()' },
                { label: 'unique count', method: 'unique()' },
                { label: 'sum', method: 'sum()' },
                { label: 'average', method: 'mean()' },
                { label: 'min', method: 'min()' },
                { label: 'max', method: 'max()' }
            ]
        }
    }

    return {
        initOption: initOption
    };
});