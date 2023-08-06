define([
    'require'
    , 'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    , 'nbextensions/visualpython/src/common/vpFuncJS'
], function (requirejs, $, vpCommon, vpConst, sb, vpFuncJS) {
    // 옵션 속성
    const funcOptProp = {
        stepCount : 1
        , funcName : "pip"
        , funcID : "com_pip"
        , funcArgs : [
            
        ]
    }

    /**
     * html load 콜백. 고유 id 생성하여 부과하며 js 객체 클래스 생성하여 컨테이너로 전달
     * @param {function} callback 호출자(컨테이너) 의 콜백함수
     * @param {JSON} meta 메타 데이터
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
            var pipPackage = new PipPackage(uuid);
            pipPackage.metadata = meta;
            
            // 옵션 속성 할당.
            pipPackage.setOptionProp(funcOptProp);
            // html 설정.
            pipPackage.initHtml();
            callback(pipPackage);  // 공통 객체를 callback 인자로 전달
        }
    }
    
    /**
     * html 로드. 
     * @param {function} callback 호출자(컨테이너) 의 콜백함수
     * @param {JSON} meta 메타 데이터
     */
    var initOption = function(callback, meta) {
        vpCommon.loadHtml(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.OPTION_GREEN_ROOM)), "file_io/pip.html", optionLoadCallback, callback, meta);
    }

    /**
     * 본 옵션 처리 위한 클래스
     * @param {String} uuid 고유 id
     */
    var PipPackage = function(uuid) {
        this.uuid = uuid;   // Load html 영역의 uuid.
        this.package = {
            input: [
                { name: 'vp_pipMeta' }
            ]
        };
        // alert on changing --yes option with uninstall
        this.alertOnOption = true;
    }

    /**
     * vpFuncJS 에서 상속
     */
    PipPackage.prototype = Object.create(vpFuncJS.VpFuncJS.prototype);

    /**
     * 유효성 검사
     * @returns 유효성 검사 결과. 적합시 true
     */
    PipPackage.prototype.optionValidation = function() {
        return true;

        // 부모 클래스 유효성 검사 호출.
        // vpFuncJS.VpFuncJS.prototype.optionValidation.apply(this);
    }

    PipPackage.prototype.getMetadata = function(id) {
        if (this.metadata == undefined)
            return "";
        var len = this.metadata.options.length;
        for (var i = 0; i < len; i++) {
            var obj = this.metadata.options[i];
            if (obj.id == id)
                return obj.value;
        }
        return "";
    }

    /**
     * html 내부 binding 처리
     */
    PipPackage.prototype.initHtml = function() {
        var that = this;

        this.loadCss(Jupyter.notebook.base_url + vpConst.BASE_PATH + vpConst.STYLE_PATH + "file_io/pip.css");
        
        var sbPageContent = new sb.StringBuilder();
        var sbTagString = new sb.StringBuilder();

        // prefix code 입력 영역
        sbPageContent.appendLine(this.createManualCode(vpConst.API_OPTION_PREFIX_CAPTION, vpConst.API_OPTION_PREFIX_CODE_ID));

        // TODO: 필수 옵션 테이블 레이아웃
        var tblLayoutRequire = this.createVERSimpleLayout("10%");
        tblLayoutRequire.addClass(vpConst.OPTION_TABLE_LAYOUT_HEAD_HIGHLIGHT);
        tblLayoutRequire.addClass('vp-pip-table');

        var addRowList = [];
        // TODO: load metadata
        var decodedMeta = decodeURIComponent(that.getMetadata('vp_pipMeta'));
        if (decodedMeta != "") {
            var colMeta = JSON.parse(decodedMeta);
            // load column data
            for (var i = 0; i < colMeta.length; i++) {
                // checkbox
                sbTagString.clear();
                sbTagString.appendLine("<label>");
                sbTagString.appendFormatLine("<input type='checkbox' class='vp-pip-comment' {0} />", colMeta[i]['vp-pip-comment']?"checked":"");
                sbTagString.appendFormatLine("<span title='{0}'>pip</span></label>", "Check to comment this command");

                var header = sbTagString.toString();

                sbTagString.clear();
                sbTagString.appendFormatLine("<input type='text' class='vp-pip-command' placeholder='{0}' value='{1}'/>", "[command]", colMeta[i]['vp-pip-command']);
                sbTagString.appendFormatLine("<input type='text' class='vp-pip-pkgn' placeholder='{0}' value='{1}'/>", "[package]", colMeta[i]['vp-pip-pkgn']);
                sbTagString.appendFormatLine("<input type='text' class='vp-pip-opt' placeholder='{0}' value='{1}'/>", "[option]", colMeta[i]['vp-pip-opt']);
                sbTagString.appendLine("<div class='vp-icon-btn vp-pip-del'></div>");
                addRowList.push([header, sbTagString.toString()]);
            }
        } else {
            // checkbox
            sbTagString.clear();
            sbTagString.appendLine("<label>");
            sbTagString.appendLine("<input type='checkbox' class='vp-pip-comment' />");
            sbTagString.appendFormatLine("<span title='{0}'>pip</span></label>", "Check to comment this command");

            var header = sbTagString.toString();
            
            // input text (command, package, option)
            sbTagString.clear();
            sbTagString.appendFormatLine("<input type='text' class='vp-pip-command' placeholder='{0}'/>", "[command]");
            sbTagString.appendFormatLine("<input type='text' class='vp-pip-pkgn' placeholder='{0}'/>", "[package]");
            sbTagString.appendFormatLine("<input type='text' class='vp-pip-opt' placeholder='{0}'/>", "[option]");
            sbTagString.appendLine("<div class='vp-icon-btn vp-pip-del'></div>");
            addRowList.push([header, sbTagString.toString()]);
        }

        addRowList.forEach(row => {
            tblLayoutRequire.addRow(row[0], row[1]);
        });

        // add button
        sbTagString.clear();
        sbTagString.appendFormatLine("<input type='button' id='{0}' class='vp-pip-add-btn' value='{1}'/>", "vp_pipAddBtn", "+ Add Package");

        tblLayoutRequire.addRow("", sbTagString.toString());

        // 필수 옵션 영역 (아코디언 박스)
        var accBoxRequire = this.createOptionContainer('pip cmd package options');
        accBoxRequire.setOpenBox(true);
        accBoxRequire.appendContent(tblLayoutRequire.toTagString());
        accBoxRequire.appendContent("<input type='hidden' id='vp_pipMeta'/>");

        sbPageContent.appendLine(accBoxRequire.toTagString());

        // postfix code 입력 영역
        sbPageContent.appendLine(this.createManualCode(vpConst.API_OPTION_POSTFIX_CAPTION, vpConst.API_OPTION_POSTFIX_CODE_ID));

        // 페이지에 컨트롤 삽입 vpFuncJS 에서 제공
        $(this.wrapSelector()).append(sbPageContent.toString());

        // prefix basic code
        $(this.wrapSelector('#' + vpConst.API_OPTION_PREFIX_CODE_ID)).val('# Auto-Generated by VisualPython - Common > pip');

        // autocomplete
        var commandSource = ['help', 'install', 'uninstall', 'list', 'show', 'search'];
        var pkgnSource = {
            'help': ['install', 'uninstall', 'list', 'show', 'search'],
            'other': ['pandas', 'numpy', 'matplotlib', 'seaborn', 'scikit-learn', '--help'],
        };
        var optSource = {
            'install': ['--verbose'],
            'uninstall': ['--yes'],
            'other': []
        };
        
        $(this.wrapSelector('.vp-pip-command')).autocomplete({
            source: commandSource,
            autoFocus: true
        });
        $(this.wrapSelector('.vp-pip-pkgn')).autocomplete({
            source: function (request, response) {
                var data = request.term;
                var cmd = $(this.element).closest('tr').find('.vp-pip-command').val();
                if (cmd != 'help') {
                    cmd = 'other';
                }
                var filteredSource = pkgnSource[cmd].filter(x => (x.indexOf(data) >= 0));
                response($.map(filteredSource, function (item) {
                    return item;
                }))
            },
            autoFocus: true
        });
        $(this.wrapSelector('.vp-pip-opt')).autocomplete({
            source: function (request, response) {
                var data = request.term;
                var cmd = $(this.element).closest('tr').find('.vp-pip-command').val();
                if (cmd != 'install' && cmd != 'uninstall') {
                    cmd = 'other';
                }
                var filteredSource = optSource[cmd].filter(x => (x.indexOf(data) >= 0));
                response($.map(filteredSource, function (item) {
                    return item;
                }))
            },
            autoFocus: true
        });
        

        // 이벤트 처리
        // E1. Add Package
        $(this.wrapSelector('#vp_pipAddBtn')).click(function() {
            // tblLayoutRequire.addRow(header, inputTag);
            sbTagString.clear();
            sbTagString.appendLine("<label>");
            sbTagString.appendLine("<input type='checkbox' class='vp-pip-comment' />");
            sbTagString.appendFormatLine("<span title='{0}'>pip</span></label>", "Check to comment this command");

            var header = sbTagString.toString();
            
            // input text (command, package, option)
            sbTagString.clear();
            sbTagString.appendFormatLine("<input type='text' class='vp-pip-command' placeholder='{0}'/>", "[command]");
            sbTagString.appendFormatLine("<input type='text' class='vp-pip-pkgn' placeholder='{0}'/>", "[package]");
            sbTagString.appendFormatLine("<input type='text' class='vp-pip-opt' placeholder='{0}'/>", "[option]");
            sbTagString.appendLine("<div class='vp-icon-btn vp-pip-del'></div>");

            var inputTag = sbTagString.toString();

            var rowString = $(vpCommon.formatString("<tr><th>{0}</th><td>{1}</td></tr>", header, inputTag));

            rowString.insertBefore($(that.wrapSelector('.vp-pip-table tr:last')));

            // autocomplete set
            rowString.find('.vp-pip-command').autocomplete({
                source: commandSource,
                autoFocus: true
            });
            rowString.find('.vp-pip-pkgn').autocomplete({
                source: function (request, response) {
                    var data = request.term;
                    var cmd = $(this.element).closest('tr').find('.vp-pip-command').val();
                    if (cmd != 'help') {
                        cmd = 'other';
                    }
                    var filteredSource = pkgnSource[cmd].filter(x => (x.indexOf(data) >= 0));
                    response($.map(filteredSource, function (item) {
                        return item;
                    }))
                },
                autoFocus: true
            });
            rowString.find('.vp-pip-opt').autocomplete({
                source: function (request, response) {
                    var data = request.term;
                    var cmd = $(this.element).closest('tr').find('.vp-pip-command').val();
                    if (cmd != 'install' && cmd != 'uninstall') {
                        cmd = 'other';
                    }
                    var filteredSource = optSource[cmd].filter(x => (x.indexOf(data) >= 0));
                    response($.map(filteredSource, function (item) {
                        return item;
                    }))
                },
                autoFocus: true
            });
        });

        // E2. Delete Package
        $(document).on('click', this.wrapSelector('.vp-pip-del'), function() {
            // if one left, just clear it
            if ($(that.wrapSelector('.vp-pip-table tr:not(:last)')).length <= 1) {
                // clear
                $(this).closest('tr').find('.vp-pip-command').val('');
                $(this).closest('tr').find('.vp-pip-pkgn').val('');
                $(this).closest('tr').find('.vp-pip-opt').val('');
            } else {
                // delete it
                $(this).closest('tr').remove();
            }
        });

        // E3. command change
        $(document).on('change', this.wrapSelector('.vp-pip-command'), function() {
            var val = $(this).val();
            if (val == 'install') {
                $(this).closest('tr').find('.vp-pip-opt').val('--verbose');
            } else if (val == 'uninstall') {
                $(this).closest('tr').find('.vp-pip-opt').val('--yes');
            }
        });

        // uninstall --yes : alert when user try to change it
        $(document).on('change', this.wrapSelector('.vp-pip-opt'), function() {
            var cmd = $(this).parent().find('.vp-pip-command').val();
            var val = $(this).val();
            if (cmd == 'uninstall' && val != '--yes' && that.alertOnOption == true) {
                // alert when user try to change --yes option
                vpCommon.renderAlertModal("'--yes' option is recommended for jupyter notebook environment");
                // don't show it again (FIXME: is it ok?)
                that.alertOnOption = false;
            }
        });
        
    }

    /**
     * 코드 생성
     * @param {boolean} addCell 셀에 추가
     * @param {boolean} exec 실행여부
     */
    PipPackage.prototype.generateCode = function(addCell = false, exec = false) {
        var code = new sb.StringBuilder();

        code.appendFormatLine('{0}', $(this.wrapSelector('#' + vpConst.API_OPTION_PREFIX_CODE_ID)).val());
        
        // code from user input
        var inputs = $(this.wrapSelector('.vp-pip-table tr:not(:last)'));
        // metadata save
        var pipMeta = [];
        for (var i = 0; i < inputs.length; i++) {
            var comment = $(inputs[i]).find('.vp-pip-comment').prop('checked');
            var cmd = $(inputs[i]).find('.vp-pip-command').val();
            var pkgn = $(inputs[i]).find('.vp-pip-pkgn').val();
            var opt = $(inputs[i]).find('.vp-pip-opt').val();

            var commentVal = comment ? "#" : "";

            if (i > 0) {
                code.appendLine();
            }
            code.appendFormat('{0}!pip {1} {2} {3}', commentVal, cmd, pkgn, opt);

            // save metadata for package list
            pipMeta.push({
                'vp-pip-comment': comment,
                'vp-pip-command': cmd,
                'vp-pip-pkgn': pkgn,
                'vp-pip-opt': opt
            });
        }

        // save column metadata
        $(this.wrapSelector('#vp_pipMeta')).val(encodeURIComponent(JSON.stringify(pipMeta)));

        code.appendFormat('{0}', $(this.wrapSelector('#' + vpConst.API_OPTION_POSTFIX_CODE_ID)).val());

        if (addCell) {
            this.cellExecute(code.toString(), exec);
        }

        return code.toString();
    }

    return {
        initOption: initOption
    };
});
