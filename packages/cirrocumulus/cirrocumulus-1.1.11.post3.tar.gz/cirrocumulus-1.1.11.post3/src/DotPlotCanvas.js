import {Tooltip, withStyles} from '@material-ui/core';
import FormControl from '@material-ui/core/FormControl';
import IconButton from '@material-ui/core/IconButton';
import Input from '@material-ui/core/Input';
import InputLabel from '@material-ui/core/InputLabel';
import Menu from '@material-ui/core/Menu';
import MenuItem from '@material-ui/core/MenuItem';
import Select from '@material-ui/core/Select';
import Typography from '@material-ui/core/Typography';
import PhotoCameraIcon from '@material-ui/icons/PhotoCamera';
import React from 'react';
import {drawColorScheme} from './ColorSchemeLegend';
import {numberFormat, numberFormat2f} from './formatters';
import {drawSizeLegend} from './SizeLegend';

const styles = theme => ({
    root: {},
    formControl: {
        display: 'block',
        margin: theme.spacing(1),
    }

});

let svgFont = '12px Helvetica,Arial,sans-serif';
let canvasFont = '12px Roboto Condensed,Helvetica,Arial,sans-serif';


class DotPlotCanvas extends React.PureComponent {

    constructor(props) {
        super(props);
        this.divRef = React.createRef();
        this.tooltipElementRef = React.createRef();
        this.canvas = null;
        this.state = {saveImageEl: null};
    }

    onSortOrderChanged = (event) => {
        this.props.onSortOrderChanged(event.target.value);
    };

    redraw() {

        if (this.props.data == null) {
            return <div/>;
        }
        let devicePixelRatio = 1;
        if (typeof window !== 'undefined' && 'devicePixelRatio' in window) {
            devicePixelRatio = window.devicePixelRatio;
        }

        if (this.canvas == null) {
            let onMouseMove = (event) => {
                const node = event.target;
                const maxRadius = this.props.sizeScale.range()[1];
                var rect = node.getBoundingClientRect();
                let xy = [event.clientX - rect.left - node.clientLeft, event.clientY - rect.top - node.clientTop];
                // xy[0] /= devicePixelRatio;
                // xy[1] /= devicePixelRatio;
                const col = Math.floor((xy[0] - this.size.x) / (maxRadius * 2));
                const row = Math.floor((xy[1]) / (maxRadius * 2));

                if (col >= 0 && col < this.props.data[0].length && row >= 0 && row < this.props.data.length) {
                    this.tooltipElementRef.current.innerHTML = '';
                    const array = this.props.data[row];
                    const mean = array[col].mean;
                    const fractionExpressed = array[col].fractionExpressed;
                    // const renamedCategories = this.props.renamedCategories || {};
                    // const categories = this.categories;
                    // let category = categories[this.categoryOrder[row]];
                    // let newName = renamedCategories[category];
                    // if (newName != null) {
                    //     category = newName;
                    // }
                    let meanFormatted = numberFormat2f(mean);
                    if (meanFormatted.endsWith('.00')) {
                        meanFormatted = meanFormatted.substring(0, meanFormatted.lastIndexOf('.'));
                    }
                    let percentExpressed = numberFormat(100 * fractionExpressed);
                    if (percentExpressed.endsWith('.0')) {
                        percentExpressed = percentExpressed.substring(0, percentExpressed.lastIndexOf('.'));
                    }
                    this.tooltipElementRef.current.innerHTML = 'mean: ' + meanFormatted + ', % expressed: ' + percentExpressed;
                } else {
                    this.tooltipElementRef.current.innerHTML = '';
                }
            };
            let onMouseOut = (event) => {
                this.tooltipElementRef.current.innerHTML = '';

            };
            // onMouseMove = throttle(onMouseMove);
            this.canvas = document.createElement('canvas');
            this.canvas.addEventListener("mousemove", onMouseMove);
            this.canvas.addEventListener("mouseout", onMouseOut);
            this.divRef.current.append(this.canvas);
        }

        const height = this.size.height + this.size.y;
        const width = this.size.width + this.size.x;
        let canvas = this.canvas;
        const context = canvas.getContext('2d');
        canvas.width = width * devicePixelRatio;
        canvas.height = height * devicePixelRatio;
        canvas.style.width = width + 'px';
        canvas.style.height = height + 'px';
        context.font = canvasFont;

        context
            .clearRect(0, 0, width * devicePixelRatio, height * devicePixelRatio);
        context.scale(devicePixelRatio, devicePixelRatio);
        this.drawContext(context);
    }

    drawContext(context) {
        const renamedCategories = this.props.renamedCategories || {};
        const data2d = this.props.data;
        const colorScale = this.props.colorScale;
        const sizeScale = this.props.sizeScale;
        const drawCircles = this.props.drawCircles;
        const textColor = this.props.textColor;
        const maxRadius = sizeScale.range()[1];
        let diameter = maxRadius * 2;
        // context.strokeStyle = gridColor;
        // context.lineWidth = gridThickness;

        data2d.forEach((array, j) => { // each category
            const ypix = j * diameter + (drawCircles ? maxRadius : 0);
            for (let i = 0; i < array.length; i++) { // each feature
                const mean = array[i].mean;
                const color = colorScale(mean);
                context.fillStyle = color;
                context.beginPath();
                if (drawCircles) {
                    const xpix = i * diameter + maxRadius + this.size.x;
                    const frac = array[i].fractionExpressed;
                    context.arc(xpix, ypix, sizeScale(frac), 0, 2 * Math.PI);
                } else {
                    const xpix = i * diameter + this.size.x;
                    context.rect(xpix, ypix, diameter, diameter);
                }
                context.fill();
                // context.stroke();
            }
        });
        // context.lineWidth = 1;
        context.textAlign = 'right';
        context.fillStyle = textColor;
        context.textBaseline = 'middle';

        data2d.forEach((array, i) => {
            let category = array[0].name;
            let newName = renamedCategories[category];
            if (newName != null) {
                category = newName;
            }
            const pix = i * diameter + maxRadius;
            context.fillText(category, this.size.x - 4, pix);
        });
        context.textAlign = 'right';
        context.textBaseline = 'top';

        data2d[0].forEach((item, i) => {
            const text = item.feature;
            const pix = i * diameter;
            context.save();
            context.translate(this.size.x + pix + 4, this.size.height);
            context.rotate(-Math.PI / 2);
            context.fillText(text, 0, 0);
            context.restore();
        });


        // context.strokeStyle = gridColor;
        // context.lineWidth = gridThickness;
        //
        //
        // for (let i = 0; i < categories.length; i++) {
        //     const ypix = i * diameter;
        //     context.beginPath();
        //     context.moveTo(this.size.x + 2, ypix);
        //     context.lineTo(width, ypix);
        //     context.stroke();
        // }
        // for (let i = 0; i < features.length; i++) {
        //     const xpix = i * diameter + this.size.x + 2;
        //     context.beginPath();
        //     context.moveTo(xpix, 0);
        //     context.lineTo(xpix, dotplotHeight);
        //     context.stroke();
        // }

        context.setTransform(1, 0, 0, 1, 0, 0);

    }


    componentDidUpdate(prevProps, prevState, snapshot) {
        this.redraw();
    }

    componentDidMount() {
        this.redraw();
    }

    getSize(context) {
        let maxFeatureWidth = 0;
        const renamedCategories = this.props.renamedCategories || {};
        const array2d = this.props.data;
        array2d[0].forEach(item => {
            maxFeatureWidth = Math.max(maxFeatureWidth, context.measureText(item.feature).width);
        });
        maxFeatureWidth += 4;
        let xoffset = 0;

        array2d.forEach(array => {
            let category = array[0].name;
            let renamed = renamedCategories[category];
            if (renamed != null) {
                category = renamed;
            }
            xoffset = Math.max(xoffset, context.measureText(category).width);
        });
        xoffset += 4;
        const maxRadius = this.props.sizeScale.range()[1];
        const diameter = maxRadius * 2;
        const height = array2d.length * diameter + 4;
        const width = array2d[0].length * diameter + 4;
        return {x: xoffset, y: maxFeatureWidth, width: width, height: height};
    }

    update() {
        const canvas = document.createElement('canvas');
        const context = canvas.getContext('2d');
        context.font = canvasFont;
        this.size = this.getSize(context);
    }

    handleSaveImageMenu = (event) => {
        this.setState({saveImageEl: event.currentTarget});
    };
    handleSaveImageMenuClose = (event) => {
        this.setState({saveImageEl: null});
    };


    handleSaveImage = (format) => {
        this.setState({saveImageEl: null});
        let context;

        let canvas;
        if (format === 'svg') {
            context = new window.C2S(10, 10);
            context.font = svgFont;
        } else {
            canvas = document.createElement('canvas');
            context = canvas.getContext('2d');
            context.font = canvasFont;
        }

        const size = this.getSize(context);

        const colorScaleHeight = 40;
        const sizeScaleHeight = 40;
        const height = size.height + size.y + colorScaleHeight + sizeScaleHeight + 10;
        const width = Math.max(200, size.width + size.x);
        let scale = 1;
        if (format === 'svg') {
            context = new window.C2S(width, height);
            context.font = svgFont;
        } else {
            canvas.width = width * window.devicePixelRatio;
            canvas.height = height * window.devicePixelRatio;
            context = canvas.getContext('2d');
            scale = window.devicePixelRatio;
            context.scale(window.devicePixelRatio, window.devicePixelRatio);
            context.font = canvasFont;
        }
        const textColor = this.props.textColor;
        if (textColor === 'white') {
            context.fillStyle = 'black';
            context.fillRect(0, 0, width, height);
        }
        this.drawContext(context);

        // if (format !== 'svg') {
        //     context.scale(window.devicePixelRatio, window.devicePixelRatio);
        // }

        context.translate(scale * 10, scale * (size.height + size.y + 4));
        drawColorScheme(context, 150, colorScaleHeight, this.props.colorScale, true, 10, textColor);

        context.translate(-10, (colorScaleHeight + 4));

        drawSizeLegend(context, this.props.sizeScale, 3, 150, 20, textColor);

        if (format === 'svg') {
            let svg = context.getSerializedSvg();
            // let prefix = [];
            // prefix.push('<?xml version="1.0" encoding="utf-8"?>\n');
            // prefix.push('<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"' +
            //     ' "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n');
            // svg = prefix.join('') + svg;
            let blob = new Blob([svg], {
                type: 'text/plain;charset=utf-8'
            });
            window.saveAs(blob, this.dotplot.name + '.svg');
        } else {
            canvas.toBlob(blob => {
                window.saveAs(blob, this.dotplot.name + '.png', true);
            });
        }
    };

    render() {
        this.update();
        const {saveImageEl} = this.state;
        const array2d = this.props.data;
        const sortBy = this.props.sortBy;
        const dimension = array2d[0][0].dimension;
        const features = array2d[0].map(item => item.feature);
        const sortChoices = [array2d[0][0].dimension].concat(features);
        return (<div style={{position: 'relative'}}>
            <div>
                <Typography style={{display: 'inline-block'}} component={"h4"}
                            color="textPrimary">{dimension}{this.props.subtitle &&
                <small>({this.props.subtitle})</small>}</Typography>
                <Tooltip title={"Save Image"}>
                    <IconButton aria-controls="save-image-menu" aria-haspopup="true" edge={false}
                                size={'small'}
                                aria-label="Save Image" onClick={this.handleSaveImageMenu}>
                        <PhotoCameraIcon/>
                    </IconButton>
                </Tooltip>
                <Menu
                    id="save-image-menu"
                    anchorEl={saveImageEl}
                    keepMounted
                    open={Boolean(saveImageEl)}
                    onClose={this.handleSaveImageMenuClose}
                >
                    <MenuItem onClick={e => this.handleSaveImage('png')}>PNG</MenuItem>
                    <MenuItem onClick={e => this.handleSaveImage('svg')}>SVG</MenuItem>

                </Menu>

                <Typography color="textPrimary" className="cirro-condensed" ref={this.tooltipElementRef} style={{
                    display: 'inline-block',
                    paddingLeft: 5,
                    verticalAlign: 'top',
                    whiteSpace: 'nowrap',
                    width: 500,
                    minWidth: 500,
                    maxWidth: 500,
                    textOverflow: 'ellipsis'
                }}></Typography>

                {this.props.onSortOrderChanged ? <FormControl className={this.props.classes.formControl}>
                    <InputLabel shrink={true}>Sort By</InputLabel>
                    <Select

                        input={<Input size={"small"}/>}
                        onChange={this.onSortOrderChanged}
                        value={sortBy}
                    >
                        {sortChoices.map(item => (
                            <MenuItem key={item} value={item}>{item}</MenuItem>
                        ))}
                    </Select>
                </FormControl> : null}
            </div>
            <div ref={this.divRef}></div>

        </div>);

    }
}

export default withStyles(styles)(DotPlotCanvas);


