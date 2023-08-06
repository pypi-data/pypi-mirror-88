SCRIPT="""
<div id="%(id)s" style="display:none;" class="%(class)s">&nbsp;</div>
<script type="text/javascript">
    var flashvars = {};

    //////////////////////////////////////////////////////////////////////////////////////////////////////
    // CUSTUMIZABLE PARAMETERS ///////////////////////////////////////////////////////////////////////
    //////////////////////////////////////////////////////////////////////////////////////////////////////

    // video width
    var stageW = %(width)s;

    // video height        NOTE: you should include the control bar height
    var stageH = %(height)s;

    ///////////////////////////////////////////////////////////////////////
    // PATHS //////////////////////////////////////////////////////////////
    ///////////////////////////////////////////////////////////////////////

    // image path
    flashvars.imagePath            = "%(backgroundImage)s";

    // video path
    flashvars.videoPath         = "%(url)s";

    // video title
    flashvars.title             = "%(title)s";

    // video description
    flashvars.description         = "%(description)s";

    ///////////////////////////////////////////////////////////////////////
    // VIEW CONTROLS ////////////////////////////////////////////////////
    ///////////////////////////////////////////////////////////////////////

    // view information button          NOTE: this will display the title and description of the video
    flashvars.viewInfoButton         =    "false";

    // view fullscreen button        ( true / false )
    flashvars.viewFullscreenButton     =    "true";

    // view scale button            ( true / false )
    flashvars.viewScaleButton         =    "true";

    // view volume controls            ( true / false )
    flashvars.viewVolumeControls     =    "false";

    // view video time                ( true / false )
    flashvars.viewTime                =    "false";

    // view big middle button        ( true / false )
    flashvars.viewBigPlayButton     =    "false";

    // view right click menu        ( true / false )
    flashvars.viewRightClickMenu     =    "false";

    ////////////////////////////////////////////////////////////////////////
    // MOUSE FUNCTIONS //////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////

    // mouse hide                            ( true / false )
    flashvars.mouseHide                =    "true";

    // mouse hide after # (seconds)        NOTE : Must be a hole number !
    flashvars.mouseHideTime            =    "2";

    // double click for toggle size view    ( true / false )
    flashvars.doubleClick            =    "true";

    // click the video for play/pause        ( true / false )
    flashvars.oneClick                =    "true";

    ////////////////////////////////////////////////////////////////////////
    // KEYBOARD FUNCTIONS ///////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////

    // play/pause on SPACE key         ( true / false )
    flashvars.spaceKey                =    "true";

    ////////////////////////////////////////////////////////////////////////
    // VIDEO FUNCTIONS ///////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////

    // video loop                ( true / false )
    flashvars.videoLoop            =    "false";

    // video auto play            ( true / false )
    flashvars.videoAutoPlay        =    "false";

    // video buffer time        ( seconds )
    flashvars.videoBufferTime    =    "0.1";

    // timeline interval
    flashvars.tlInterval        =    "100000";

    // sound volume at start         NOTE :    1=Max    0=Min
    flashvars.soundVolume        =    "0.8";

    // size the video starts at
    // can be set to 1, 2 and 3
    // 1 for narmol size view
    // 2 for aspect view
    // 3 for full size view
    flashvars.fullSizeView        =    "1";

    ////////////////////////////////////////////////////////////////////////
    // VISUAL APPEARANCE  /////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////

    // spacing between the controls
    flashvars.spacing             =    "0";

    // control bar height        ( height )
    flashvars.controlHeight        =    "20";

    // vulume scrub lenght         ( lenght )
    flashvars.volumeLengthW        =     "0";

    // controls background        ( colors / alphas )
    flashvars.color1             =     "0xcccccc";
    flashvars.color2             =     "0xffffff";
    flashvars.alpha1             =     "1";
    flashvars.alpha2             =     "1";

    // controls border            ( color / alpha )
    flashvars.borderColor         =     "0xcccccc";
    flashvars.borderAlpha        =     "1";

    // time view ////////////////////////////////////
    // time view background        ( colors / alphas )
    flashvars.timeColor1        =     "0x333333";
    flashvars.timeColor2        =     "0x111111";
    flashvars.timeAlpha1        =     "1";
    flashvars.timeAlpha2        =     "1";

    // time view text color        ( color )
    flashvars.timeTextColor1    =     "0xffffff";
    flashvars.timeTextColor2    =     "0x888888";


    // scrubber /////////////////////////////////////////////////////
    // scrubber height            ( height )
    flashvars.scrubberHeight     =    "3";

    // scrubber background         ( color / alpha )
    flashvars.scrubberColor1    =     "0xcccccc";
    flashvars.scrubberAlpha1    =     "1";

    // scrubber                    ( color / alpha )
    flashvars.scrubberColor2    =     "0x47d2ff";
    flashvars.scrubberAlpha2    =     "1";

    // scrubber glow filter        ( color / alpha )
    flashvars.filterColor        =     "0x0066ff";
    flashvars.filterAlpha        =     "1";

    // control buttons    ///////////////////////////////////////////////
    // control buttons color    ( color )
    //flashvars.buttonColor        =     "0x000000";

    // info view /////////////////////////////////////////////////////
    // title color                    ( color )
    flashvars.titleColor            =    "0x47d2ff";

    // description color            ( color )
    flashvars.descriptionColor        =    "0xD3D3D3";

    // info background                ( color / alpha )
    flashvars.infoBackgroundColor    =    "0x000000";
    flashvars.infoBackgroundAlpha    =    "0.5";

    //////////////////////////////////////////////////////////////////////////////////////////////////////
    //////////////////////////////////////////////////////////////////////////////////////////////////////
    //////////////////////////////////////////////////////////////////////////////////////////////////////

    var params = {wmode: "transparent"};
    params.scale = "noscale";
    params.allowfullscreen = "true";
    params.salign = "tl";
    params.bgcolor = "000000";
    params.allowscriptaccess = "always";

    var attributes = {};
    swfobject.embedSWF("./++resource++swfplayer/player.swf", "%(id)s", stageW, stageH, "9.0.0", false, flashvars, params, attributes);
</script>
"""

HTML="""
    <object data="%(portalUrl)s/++resource++swfplayer/player.swf" type="application/x-shockwave-flash" height="%(height)s" width="%(width)s">
        <param name="wmode" value="transparent"/>
        <param name="scale" value="noscale"/>
        <param name="allowfullscreen" value="true"/>
        <param name="salign" value="tl"/>
        <param name="bgcolor" value="000000"/>
        <param name="allowscriptaccess" value="always"/>
        <param name="movie" value="%(portalUrl)s/++resource++swfplayer/player.swf"/>
        <param name="flashvars" value="imagePath=%(backgroundImage)s&amp;videoPath=%(url)s&amp;title=%(title)s&amp;description=%(description)s&amp;viewInfoButton=false&amp;viewFullscreenButton=true&amp;viewScaleButton=true&amp;viewVolumeControls=false&amp;viewTime=false&amp;viewBigPlayButton=false&amp;viewRightClickMenu=false&amp;mouseHide=true&amp;mouseHideTime=2&amp;doubleClick=true&amp;oneClick=true&amp;spaceKey=true&amp;videoLoop=false&amp;videoAutoPlay=false&amp;videoBufferTime=0.1&amp;tlInterval=100000&amp;soundVolume=0.8&amp;fullSizeView=1&amp;spacing=0&amp;controlHeight=20&amp;volumeLengthW=0&amp;color1=0xcccccc&amp;color2=0xffffff&amp;alpha1=1&amp;alpha2=1&amp;borderColor=0xcccccc&amp;borderAlpha=1&amp;timeColor1=0x333333&amp;timeColor2=0x111111&amp;timeAlpha1=1&amp;timeAlpha2=1&amp;timeTextColor1=0xffffff&amp;timeTextColor2=0x888888&amp;scrubberHeight=3&amp;scrubberColor1=0xcccccc&amp;scrubberAlpha1=1&amp;scrubberColor2=0x47d2ff&amp;scrubberAlpha2=1&amp;filterColor=0x0066ff&amp;filterAlpha=1&amp;titleColor=0x47d2ff&amp;descriptionColor=0xD3D3D3&amp;infoBackgroundColor=0x000000&amp;infoBackgroundAlpha=0.5"/>
    </object>
"""