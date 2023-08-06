define([
    'require'
    , 'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    , 'nbextensions/visualpython/src/common/component/vpComComponent'
], function (requirejs, $, vpCommon, vpConst, sb, vpComComponent) {
    /**
     * @class vpLineNumberTextArea 라인넘버 textarea
     * @constructor
     * @param {String} compID 입력 textarea id
     */
    var vpLineNumberTextArea = function(compID = "", content = "") {
        this.setUUID();
        this._compID = compID;
        this._content = content;
        this._attributes = "";
    };

    vpLineNumberTextArea.prototype = Object.create(vpComComponent.vpComComponent.prototype);

    /**
     * 입력 textarea id
     * @param {String} compID 입력 textarea id
     */
    vpLineNumberTextArea.prototype.setComponentID = function(compID = "") {
        this._compID = compID;
    }

    /**
     * textarea 컨텐츠 내용 preppend
     * @param {String} content contents
     */
    vpLineNumberTextArea.prototype.setContent = function(content = "") {
        this._content = content;
    }

    /**
     * 라인넘버 textarea 추가 속성 부여
     * @param {String} attrName 속성명
     * @param {String} attrValue 속성값
     */
    vpLineNumberTextArea.prototype.addAttribute = function(attrName = "", attrValue = "") {
        if (attrName == "") return;
        var that = this;
        that._attributes = vpCommon.formatString("{0} {1}='{2}'", that._attributes, attrName, attrValue);
    }
    /**
     * 라인넘버 textarea 태그 생성
     * @returns html 라인넘버 textarea tag string
     */
    vpLineNumberTextArea.prototype.toTagString = function() {
        var sbTagString = new sb.StringBuilder();
        var that = this;
        var scrollSyncFunc = "function vpLNTAscrollSync(trg) {trg.parentElement.parentElement.getElementsByTagName(\"textarea\")[0].scrollTop = trg.scrollTop; } vpLNTAscrollSync(this)";

        sbTagString.appendFormatLine("<div class='{0}' {1}>"
            , that._UUID, that._attributes);

        sbTagString.appendFormat("<textarea class='{0}' readonly>1</textarea>", vpConst.MANUAL_CODE_INPUT_AREA_LINE);
        sbTagString.appendFormatLine("<textarea class='{0}' {1} onscroll='{2}'>{3}</textarea>"
            , vpConst.MANUAL_CODE_INPUT_AREA, that._compID == "" ? "" : vpCommon.formatString("id='{0}'", that._compID), scrollSyncFunc, that._content);

        sbTagString.appendLine("</div>");
        
        return sbTagString.toString();
    }

    return {
        vpLineNumberTextArea: vpLineNumberTextArea
    }
});