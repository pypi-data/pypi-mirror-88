import {InputLabel, Switch} from '@material-ui/core';
import MuiAccordionPanel from '@material-ui/core/Accordion';
import MuiAccordionPanelDetails from '@material-ui/core/AccordionDetails';
import MuiAccordionPanelSummary from '@material-ui/core/AccordionSummary';
import Box from '@material-ui/core/Box';
import Button from '@material-ui/core/Button';
import Checkbox from '@material-ui/core/Checkbox';
import Chip from '@material-ui/core/Chip';
import Dialog from '@material-ui/core/Dialog';
import DialogContent from '@material-ui/core/DialogContent';
import DialogTitle from '@material-ui/core/DialogTitle';
import Divider from '@material-ui/core/Divider';
import FormControl from '@material-ui/core/FormControl';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Grid from '@material-ui/core/Grid';
import IconButton from '@material-ui/core/IconButton';
import Input from '@material-ui/core/Input';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemSecondaryAction from '@material-ui/core/ListItemSecondaryAction';
import ListItemText from '@material-ui/core/ListItemText';
import Menu from '@material-ui/core/Menu';
import MenuItem from '@material-ui/core/MenuItem';
import Select from '@material-ui/core/Select';
import Slider from '@material-ui/core/Slider';
import withStyles from '@material-ui/core/styles/withStyles';
import TextField from '@material-ui/core/TextField';
import Tooltip from '@material-ui/core/Tooltip';
import ArrowDropDownIcon from '@material-ui/icons/ArrowDropDown';
import CloudDownloadIcon from '@material-ui/icons/CloudDownload';
import DeleteIcon from '@material-ui/icons/Delete';
import FontDownloadRoundedIcon from '@material-ui/icons/FontDownloadRounded';
import HighlightOffIcon from '@material-ui/icons/HighlightOff';
import SaveIcon from '@material-ui/icons/Save';
import {debounce} from 'lodash';
import memoize from "memoize-one";
import natsort from 'natsort';
import React from 'react';
import {connect} from 'react-redux';
import {
    deleteDatasetFilter,
    deleteFeatureSet,
    downloadSelectedIds,
    exportDatasetFilters,
    getDatasetFilterArray,
    getEmbeddingKey,
    getTraceKey,
    openDatasetFilter,
    removeDatasetFilter,
    SAVE_DATASET_FILTER_DIALOG,
    SAVE_FEATURE_SET_DIALOG,
    setBinSummary,
    setBinValues,
    setChartSize,
    setCombineDatasetFilters,
    setDialog,
    setInterpolator,
    setMarkerOpacity,
    setNumberOfBins,
    setPointSize,
    setPrimaryTraceKey,
    setSearchTokens,
    setSelectedEmbedding,
    setUnselectedMarkerOpacity,
    toggleEmbeddingLabel
} from './actions';
import AutocompleteVirtualized from './AutocompleteVirtualized';
import ColorSchemeSelector from './ColorSchemeSelector';
import {intFormat} from './formatters';
import {getFeatureSets, splitSearchTokens} from './util';

const sorter = natsort();
const pointSizeOptions = [{value: 0.1, label: '10%'}, {value: 0.25, label: '25%'}, {value: 0.5, label: '50%'}, {
    value: 0.75,
    label: '75%'
}, {value: 1, label: '100%'}, {value: 1.5, label: '150%'}, {value: 2, label: '200%'}, {
    value: 3,
    label: '300%'
}, {value: 4, label: '400%'}];
const gallerySizeOptions = [{value: 300, label: 'Small'}, {value: 500, label: 'Medium'}, {
    value: 800,
    label: 'Large'
}];
const summaryOptions = [
    {value: 'max', label: 'Maximum'},
    {value: 'mean', label: 'Mean'},
    {value: 'sum', label: 'Sum'}];
const styles = theme => ({
    root: {
        display: 'flex',
        flexWrap: 'nowrap',
        width: '100%',
        flexDirection: 'column'
    },
    formControl: {
        display: 'block',
        minWidth: 200,
        margin: theme.spacing(1),
    },
    select: {
        minWidth: 200,
    },
});

const getEmbeddingKeys = memoize(
    (embeddings) => {
        const embeddingKeys = embeddings.map(e => getEmbeddingKey(e));
        embeddingKeys.sort(sorter);
        return embeddingKeys;
    }
);

const getAnnotationOptions = memoize(
    (obs, obsCat) => {
        const options = [];
        obs.forEach(item => {
            options.push({group: 'Continuous', text: item, id: item});
        });
        obsCat.forEach(item => {
            options.push({group: 'Categorical', text: item, id: item});
        });
        options.sort((item1, item2) => {
            const c = sorter(item1.group, item2.group);
            if (c !== 0) {
                return c;
            }
            return sorter(item1.text, item2.text);
        });
        return options;
    }
);
const getFeatureSetOptions = memoize((markers) => {
        const options = markers.map(item => ({group: item.category, text: item.name, id: item.id}));
        options.sort((item1, item2) => {
            const c = sorter(item1.group, item2.group);
            if (c !== 0) {
                return c;
            }
            return sorter(item1.text, item2.text);
        });
        return options;
    }
);
const Accordion = withStyles({
    root: {
        border: '1px solid rgba(0, 0, 0, .125)',
        boxShadow: 'none',
        '&:not(:last-child)': {
            borderBottom: 0,
        },
        '&:before': {
            display: 'none',
        },
        '&$expanded': {
            margin: 0,
        },
    },
    expanded: {},
})(MuiAccordionPanel);

const AccordionPanelSummary = withStyles({
    root: {
        backgroundColor: 'rgba(0, 0, 0, .03)',
        borderBottom: '1px solid rgba(0, 0, 0, .125)',
        marginBottom: -1,
        minHeight: 43,
        '&$expanded': {
            minHeight: 43,
        },
    },
    content: {
        '&$expanded': {
            margin: 0,
        },
    },
    expanded: {},
})(MuiAccordionPanelSummary);

const AccordionPanelDetails = withStyles(theme => ({
    root: {
        padding: 0,
    },
}))(MuiAccordionPanelDetails);


class SideBar extends React.PureComponent {


    constructor(props) {
        super(props);
        this.state = {
            featureSetAnchorEl: null,
            featureSet: null,
            featureSetView: false,
            opacity: props.markerOpacity,
            unselectedOpacity: props.unselectedMarkerOpacity
        };
        this.updateMarkerOpacity = debounce(this.updateMarkerOpacity, 500);
        this.updateUnselectedMarkerOpacity = debounce(this.updateUnselectedMarkerOpacity, 500);
        // this.updateNumberOfBins = debounce(this.updateNumberOfBins, 200);
    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        if (prevProps.markerOpacity !== this.props.markerOpacity) {
            this.setState({opacity: this.props.markerOpacity});
        }
        if (prevProps.unselectedMarkerOpacity !== this.props.unselectedMarkerOpacity) {
            this.setState({unselectedOpacity: this.props.unselectedMarkerOpacity});
        }
    }

    onMarkerOpacityChange = (event, value) => {

        this.setState({opacity: value});
        this.updateMarkerOpacity(value);
    };

    updateMarkerOpacity = (value) => {
        let opacity = parseFloat(value);
        if (opacity >= 0 && opacity <= 1) {
            this.props.handleMarkerOpacity(opacity);
        }
    };

    onUnselectedMarkerOpacityChange = (event, value) => {
        this.setState({unselectedOpacity: value});
        this.updateUnselectedMarkerOpacity(value);
    };

    updateUnselectedMarkerOpacity = (value) => {
        let opacity = parseFloat(value);
        if (opacity >= 0 && opacity <= 1) {
            this.props.handleUnselectedMarkerOpacity(opacity);
        }

    };


    openDatasetFilter = (filterId) => {
        this.props.handleOpenDatasetFilter(filterId);
    };

    deleteDatasetFilter = (filterId) => {
        this.props.handleDeleteDatasetFilter(filterId);
    };


    onPointSizeChange = (event) => {
        this.props.handlePointSize(event.target.value);
    };

    onFeaturesChange = (event, value) => {
        this.props.handleSearchTokens(value, 'X');
    };

    onObservationsIconClick = (event, option) => {
        this.props.handleEmbeddingLabel(option);
        event.stopPropagation();
    };

    onObservationsChange = (event, value) => {
        let values = [];
        value.forEach(val => {
            if (val.text !== undefined) {
                values.push(val.text);
            } else {
                values.push(val);
            }
        });
        this.props.handleSearchTokens(values, 'obs');
    };

    onSaveFeatureList = () => {
        this.props.handleDialog(SAVE_FEATURE_SET_DIALOG);
    };

    onFeatureSetsChange = (event, value) => {
        let values = [];
        value.forEach(val => {
            if (val.id !== undefined) {
                values.push(val.id);
            } else {
                values.push(val);
            }
        });
        this.props.handleSearchTokens(values, 'featureSet');
    };


    onFeatureSetClick = (event, option) => {
        const id = option.id;
        const target = event.target;
        let markers = this.props.markers;

        let featureSet = null;
        for (let i = 0; i < markers.length; i++) {
            if (markers[i].id === id) {
                featureSet = markers[i];
                break;
            }
        }
        if (featureSet == null) {
            console.log(id + ' not found');
        }
        event.stopPropagation();
        this.setState({featureSetAnchorEl: target, featureSet: featureSet});

    };

    onFeatureSetMenuClose = (event) => {
        this.setState({featureSetAnchorEl: null, featureSet: null});
    };

    onViewFeatureSet = (event) => {
        event.stopPropagation();
        this.setState({featureSetAnchorEl: null, featureSetView: true});
    };
    onCloseViewFeatureSetDialog = (event) => {
        event.stopPropagation();
        this.setState({featureSet: null, featureSetView: false});
    };

    onDeleteFeatureSet = (event) => {
        event.stopPropagation();
        let searchTokens = this.props.searchTokens;
        const featureSetId = this.state.featureSet.id;
        let value = searchTokens.filter(token => token.type === 'featureSet' && token.value.id !== featureSetId);
        this.props.handleSearchTokens(value, 'featureSet');
        this.props.handleDeleteFeatureSet(featureSetId);
        this.setState({featureSetAnchorEl: null, featureSet: null});
    };

    onFilterChipClicked = (event) => {
        this.onFeatureClick(event, event.target.innerText);
    };

    onFeatureClick = (event, option) => {
        event.stopPropagation();
        const value = option.text !== undefined ? option.text : option;
        let galleryTraces = this.props.embeddingData.filter(traceInfo => traceInfo.active);
        for (let i = 0; i < galleryTraces.length; i++) {
            if (galleryTraces[i].name == value) {
                this.props.handlePrimaryTraceKey(getTraceKey(galleryTraces[i]));
                break;
            }
        }
    };

    // onNumberOfBinsChange = (event) => {
    //     this.props.handleNumberOfBinsUI(event.target.value);
    //     this.updateNumberOfBins(event.target.value);
    // };
    //
    // updateNumberOfBins = (value) => {
    //
    //     value = parseInt(value);
    //     if (value >= 0) {
    //         this.props.handleNumberOfBins(value);
    //         let embeddings = this.props.embeddings;
    //         for (let i = 0; i < embeddings.length; i++) {
    //             if (!embeddings[i].precomputed) {
    //                 embeddings[i] = Object.assign(embeddings[i], {nbins: value, _nbins: value});
    //             }
    //         }
    //         this.props.handleEmbeddings(embeddings.slice(0));
    //
    //     }
    // };

    onChartSizeChange = (event) => {
        const value = event.target.value;
        this.props.handleChartSize(value);

    };

    onBinSummaryChange = (event) => {
        const value = event.target.value;
        this.props.handleBinSummary(value);
        let embeddings = this.props.embeddings;
        for (let i = 0; i < embeddings.length; i++) {
            if (!embeddings[i].precomputed) {
                embeddings[i] = Object.assign(embeddings[i], {agg: value});
            }
        }
        this.props.handleEmbeddings(embeddings.slice(0));
    };

    handleBinValuesChange = (event) => {
        const value = event.target.checked;
        this.props.handleBinValues(value);
        let embeddings = this.props.embeddings;
        for (let i = 0; i < embeddings.length; i++) {
            if (!embeddings[i].precomputed) {
                embeddings[i] = Object.assign(embeddings[i], {bin: value});
            }
        }
        this.props.handleEmbeddings(embeddings.slice(0));
    };

    handleEmbeddingsChange = (event) => {
        const embeddings = event.target.value;
        const selection = [];

        embeddings.forEach(embedding => {
            if (!embedding.precomputed) {
                embedding = Object.assign(embedding, {
                    bin: this.props.binValues,
                    nbins: this.props.numberOfBins,
                    agg: this.props.binSummary
                });
            }
            selection.push(embedding);
        });


        this.props.handleEmbeddings(selection);
    };

    handleSelectedCellsClick = (event) => {
        event.preventDefault();
        this.props.downloadSelectedIds();
    };


    onDatasetFilterChipDeleted = (name) => {
        this.props.removeDatasetFilter(name);
    };

    onDatasetFilterCleared = () => {
        this.props.removeDatasetFilter(null);
    };

    onDatasetFilterSaved = () => {
        this.props.handleDialog(SAVE_DATASET_FILTER_DIALOG);
    };

    handleCombineDatasetFilters = (event) => {
        this.props.handleCombineDatasetFilters(event.target.checked ? 'or' : 'and');
    };


    render() {
        const {
            chartSize,
            binValues,
            binSummary,
            embeddings,
            embeddingLabels,
            classes,
            searchTokens,
            datasetFilter,
            datasetFilters,
            interpolator,
            markers,
            dataset,
            pointSize,
            combineDatasetFilters,
            selection,
            serverInfo
        } = this.props;

        let currentDatasetFilters = getDatasetFilterArray(datasetFilter);
        const datasetFilterKeys = [];
        let isBrushing = false;
        currentDatasetFilters.forEach(f => {
            if (typeof f[0] === 'object') {
                isBrushing = true;
            } else {
                datasetFilterKeys.push(f[0]);
            }
        });
        datasetFilterKeys.sort((a, b) => {
            a = a.toLowerCase();
            b = b.toLowerCase();
            return a < b ? -1 : (a === b ? 0 : 1);
        });
        if (isBrushing) {
            datasetFilterKeys.push('selection');
        }

        // for filters we only need one embedding trace per feature
        // const traceNames = new Set();
        // const filterTraces = [];
        // let primaryTraceName;
        // embeddingData.forEach(trace => {
        //     if (primaryTraceKey === getTraceKey(trace)) {
        //         primaryTraceName = trace.name;
        //     }
        //     if (trace.active && trace.name !== '__count' && !traceNames.has(trace.name)) {
        //         traceNames.add(trace.name);
        //         filterTraces.push(trace);
        //     }
        // });
        // // put active trace 1st
        // filterTraces.sort((a, b) => {
        //     if (a.name === primaryTraceName) {
        //         return -1;
        //     }
        //     if (b.name === primaryTraceName) {
        //         return 1;
        //     }
        //     a = a.name.toLowerCase();
        //     b = b.name.toLowerCase();
        //     return a < b ? -1 : (a === b ? 0 : 1);
        // });


        let savedDatasetFilter = this.props.savedDatasetFilter;
        if (savedDatasetFilter == null) {
            savedDatasetFilter = {};
        }
        const splitTokens = splitSearchTokens(searchTokens);
        const featureSets = getFeatureSets(markers, splitTokens.featureSets);
        const featureOptions = dataset.features;
        const availableEmbeddings = dataset.embeddings;

        const isSummarized = dataset.precomputed != null;
        const obsCat = dataset.obsCat;
        const obs = dataset.obs;
        const embeddingKeys = getEmbeddingKeys(embeddings);
        const annotationOptions = getAnnotationOptions(obs, obsCat);
        const featureSetOptions = getFeatureSetOptions(markers);

        const fancy = serverInfo.fancy;
        const showBinPlot = false;
        const featureSetAnchorEl = this.state.featureSetAnchorEl;
        const featureSet = this.state.featureSet;
        return (
            <div className={classes.root}>
                <Dialog
                    open={this.state.featureSetView}
                    onClose={this.onCloseViewFeatureSetDialog}
                    aria-labelledby="view-set-dialog-title"
                    fullWidth={true}
                    maxWidth={'lg'}
                >
                    <DialogTitle id="view-set-dialog-title">{featureSet ? featureSet.name : ''}</DialogTitle>
                    <DialogContent>
                        <TextField
                            value={featureSet ? featureSet.features.join('\n') : ''}
                            margin="dense"
                            fullWidth
                            readonly={true}
                            variant="outlined"
                            multiline={true}
                        />
                    </DialogContent>
                </Dialog>
                <Menu
                    id="feature-set-menu"
                    anchorEl={featureSetAnchorEl}
                    open={Boolean(featureSetAnchorEl)}
                    onClose={this.onFeatureSetMenuClose}
                >
                    <MenuItem onClick={this.onViewFeatureSet}>View</MenuItem>
                    <MenuItem divider={true}/>
                    <MenuItem disabled={featureSet && featureSet.readonly}
                              onClick={this.onDeleteFeatureSet}>Delete</MenuItem>


                </Menu>
                <FormControl className={classes.formControl}>
                    <InputLabel id="embedding-label">Embeddings</InputLabel>
                    <Select
                        className={classes.select}
                        labelId="embedding-label"
                        multiple
                        value={embeddings}
                        onChange={this.handleEmbeddingsChange}
                        input={<Input/>}
                        renderValue={selected => selected.map(e => e.name + (e.dimensions === 3 ? ' 3d' : '')).join(', ')}
                    >
                        {availableEmbeddings.map(embedding => (
                            <MenuItem key={getEmbeddingKey(embedding)}
                                      value={embedding}>
                                <Checkbox checked={embeddingKeys.indexOf(getEmbeddingKey(embedding)) !== -1}/>
                                <ListItemText primary={embedding.name + (embedding.dimensions === 3 ? ' 3d' : '')}/>
                            </MenuItem>
                        ))}
                    </Select>
                </FormControl>
                {featureOptions.length > 0 && <FormControl className={classes.formControl}>

                    {/*<AutocompleteSelect label="Features" options={allOptions}*/}
                    {/*                    defaultOptions={defaultOptions} value={featureValue}*/}
                    {/*                    onChange={this.props.handleFeatures}*/}
                    {/*                    helperText={'Enter or paste list'}*/}
                    {/*                    isMulti={true}/>*/}
                    <AutocompleteVirtualized onChipClick={this.onFeatureClick} label={"Features/Genes"}
                                             options={featureOptions} value={splitTokens.X}
                                             onChange={this.onFeaturesChange}
                                             helperText={"Enter or paste list"}
                    />
                </FormControl>}

                {annotationOptions.length > 0 && <FormControl className={classes.formControl}>

                    {/*<AutocompleteSelect label="Features" options={allOptions}*/}
                    {/*                    defaultOptions={defaultOptions} value={featureValue}*/}
                    {/*                    onChange={this.props.handleFeatures}*/}
                    {/*                    helperText={'Enter or paste list'}*/}
                    {/*                    isMulti={true}/>*/}
                    <AutocompleteVirtualized label={"Cell Metadata"}
                                             options={annotationOptions}
                                             value={splitTokens.obsCat.concat(splitTokens.obs)}
                                             onChipClick={this.onFeatureClick}
                                             groupBy={true}
                                             getChipIcon={(option) => {
                                                 return splitTokens.obsCat.indexOf(option) !== -1 ?
                                                     <FontDownloadRoundedIcon
                                                         onClick={(event) => {
                                                             this.onObservationsIconClick(event, option);
                                                         }}
                                                         title={"Toggle Show/Hide Labels"}
                                                         style={{
                                                             marginLeft: 4,
                                                             marginTop: 0,
                                                             marginRight: 0,
                                                             marginBottom: 0
                                                         }}
                                                         className={"MuiChip-deleteIcon MuiChip-deleteIconSmall" + (embeddingLabels.indexOf(option) !== -1 ? ' cirro-active' : '')}/> : null;
                                             }}
                                             getOptionSelected={(option, value) => option.id === value}
                                             onChange={this.onObservationsChange}/>
                </FormControl>}


                {(fancy || featureSetOptions.length > 0) && <FormControl className={classes.formControl}>

                    <AutocompleteVirtualized label={"Sets"}
                                             options={featureSetOptions}
                                             value={featureSets}
                                             onChipClick={this.onFeatureSetClick}
                                             getChipTitle={(option) => {
                                                 return option.category;
                                             }}
                                             getChipIcon={(option) => {
                                                 return <ArrowDropDownIcon onClick={(event) => {
                                                     this.onFeatureSetClick(event, option);
                                                 }}/>;
                                             }}
                                             groupBy={true}
                                             onChange={this.onFeatureSetsChange}
                                             getOptionSelected={(option, value) => option.id === value.id}
                                             getChipText={option => option.name}/>
                    {fancy && splitTokens.X.length > 0 &&
                    <Tooltip title={"Save Current Feature List"}>
                        <IconButton size={'small'} onClick={this.onSaveFeatureList}>
                            <SaveIcon/>
                        </IconButton>
                    </Tooltip>
                    }
                </FormControl>}

                <Accordion defaultExpanded>
                    <AccordionPanelSummary
                        aria-controls="filter-content"
                        id="filter-header"
                    >
                        <div>Filters</div>
                    </AccordionPanelSummary>
                    <AccordionPanelDetails>
                        <div style={{marginLeft: 10, maxHeight: 500}}>

                            <Grid component="label" alignContent={"flex-start"} container alignItems="center"
                                  spacing={0}>
                                <Grid item><InputLabel shrink={true} variant={"standard"}>Combine
                                    Filters</InputLabel></Grid>
                                <Grid item>AND</Grid>
                                <Grid item>
                                    <Switch
                                        size="small"
                                        checked={combineDatasetFilters === 'or'}
                                        onChange={this.handleCombineDatasetFilters}
                                    />
                                </Grid>
                                <Grid item>OR</Grid>
                            </Grid>

                            {datasetFilterKeys.length > 0 && !isNaN(selection.count) &&
                            <React.Fragment>
                                <div style={{marginBottom: 2}}>
                                    {intFormat(selection.count) + " / " + intFormat(dataset.shape[0]) + ": "}
                                    {datasetFilterKeys.map(key => {
                                        return <Chip
                                            onDelete={() => {
                                                this.onDatasetFilterChipDeleted(key);
                                            }}
                                            onClick={this.onFilterChipClicked} size={"small"} variant={"default"}
                                            style={{marginRight: 2, verticalAlign: 'bottom'}}
                                            key={key}
                                            label={key}

                                        />;
                                    })}
                                    <Divider/>
                                    <Tooltip title={"Clear All"}>
                                        <IconButton size={'small'} disabled={datasetFilterKeys.length === 0}
                                                    onClick={this.onDatasetFilterCleared}><HighlightOffIcon/></IconButton>
                                    </Tooltip>
                                    {fancy && <Tooltip title={"Save Filter"}>
                                        <IconButton size={'small'} disabled={datasetFilterKeys.length === 0}
                                                    onClick={this.onDatasetFilterSaved}><SaveIcon/></IconButton>
                                    </Tooltip>}
                                    <Tooltip title={"Download Selected IDs"}>
                                        <IconButton size={'small'} disabled={datasetFilterKeys.length === 0}
                                                    onClick={this.handleSelectedCellsClick}><CloudDownloadIcon/></IconButton>
                                    </Tooltip>
                                    <Divider/>
                                </div>
                            </React.Fragment>
                            }


                        </div>
                    </AccordionPanelDetails>
                </Accordion>
                <Accordion defaultExpanded>
                    <AccordionPanelSummary
                        aria-controls="view-options-content"
                        id="view-options-header"
                    >
                        <div>View Options</div>
                    </AccordionPanelSummary>
                    <AccordionPanelDetails>
                        <div>


                            {/*<TextField type="text" onKeyPress={this.onMarkerSizeKeyPress}*/}
                            {/*           onChange={this.onMarkerSizeChange} label="Marker Size"*/}
                            {/*           className={classes.formControl} value={markerSize}/>*/}
                            {/*<TextField type="text" onKeyPress={this.onUnselectedMarkerSizeKeyPress}*/}
                            {/*           onChange={this.onUnselectedMarkerSizeChange} label="Unselected Marker Size"*/}
                            {/*           className={classes.formControl} value={unselectedMarkerSize}/>*/}
                            {/*<TextField type="text"*/}
                            {/*           onChange={this.onMarkerOpacityChange} label="Marker Opacity"*/}
                            {/*           className={classes.formControl} value={this.state.opacity}/>*/}

                            <InputLabel style={{marginLeft: 8, marginTop: 8}} shrink={true}>Marker Opacity</InputLabel>
                            <Slider
                                min={0.0}
                                max={1}
                                step={0.01}
                                style={{marginLeft: 10, width:'86%'}}
                                valueLabelDisplay="auto"
                                value={this.state.opacity}
                                onChange={this.onMarkerOpacityChange} aria-labelledby="continuous-slider"/>


                            <InputLabel style={{marginLeft: 8, marginTop: 8}} shrink={true}>Filtered Marker
                                Opacity</InputLabel>
                            <Slider
                                min={0.0}
                                max={1}
                                step={0.01}
                                style={{marginLeft: 10, width: '86%'}}
                                valueLabelDisplay="auto"
                                value={this.state.unselectedOpacity}
                                onChange={this.onUnselectedMarkerOpacityChange} aria-labelledby="continuous-slider"/>


                            <FormControl className={classes.formControl}>
                                <InputLabel htmlFor="point_size">Marker Size</InputLabel>
                                <Select
                                    className={classes.select}
                                    input={<Input id="point_size"/>}
                                    onChange={this.onPointSizeChange}
                                    value={pointSize}
                                    multiple={false}>
                                    {pointSizeOptions.map(item => (
                                        <MenuItem key={item.label} value={item.value}>
                                            <ListItemText primary={item.label}/>
                                        </MenuItem>
                                    ))}
                                </Select>
                            </FormControl>

                            <FormControl className={classes.formControl}>
                                <InputLabel htmlFor="chart_size">Gallery Chart Size</InputLabel>
                                <Select
                                    className={classes.select}
                                    input={<Input id="chart_size"/>}
                                    onChange={this.onChartSizeChange}
                                    value={chartSize}
                                    multiple={false}>
                                    {gallerySizeOptions.map(item => (
                                        <MenuItem key={item.label} value={item.value}>
                                            <ListItemText primary={item.label}/>
                                        </MenuItem>
                                    ))}
                                </Select>
                            </FormControl>

                            <FormControl className={classes.formControl}>
                                <InputLabel htmlFor="color-scheme">Color Scale</InputLabel>
                                <ColorSchemeSelector handleInterpolator={this.props.handleInterpolator}
                                                     interpolator={interpolator}/>
                            </FormControl>

                            {!isSummarized && showBinPlot && <div><FormControlLabel
                                control={
                                    <Switch
                                        checked={binValues}
                                        value={'binPlot'}
                                        onChange={this.handleBinValuesChange}
                                    />
                                }
                                label="Bin Plot"
                            /></div>}

                            {/*{!isSummarized && binValues &&*/}
                            {/*<TextField max="1000" min="20" step="100"*/}
                            {/*           value={numberOfBins}*/}
                            {/*           onChange={this.onNumberOfBinsChange} label="# Bins Per Axis"*/}
                            {/*           className={classes.formControl}/>}*/}


                            {!isSummarized && binValues && <FormControl className={classes.formControl}>
                                <InputLabel htmlFor="summary">Bin Summary</InputLabel>
                                <Select
                                    className={classes.select}
                                    input={<Input id="summary"/>}
                                    onChange={this.onBinSummaryChange}
                                    value={binSummary}
                                >
                                    {summaryOptions.map(c => (
                                        <MenuItem key={c.value} value={c.value}>
                                            <ListItemText primary={c.label}/>
                                        </MenuItem>
                                    ))}
                                </Select>
                            </FormControl>}


                            <Divider/>

                            {/*<Typography*/}
                            {/*    color="textSecondary"*/}
                            {/*    display="block"*/}
                            {/*    variant="caption"*/}
                            {/*>*/}
                            {/*    Unselected Chart Properties*/}
                            {/*</Typography>*/}


                        </div>

                    </AccordionPanelDetails>
                </Accordion>
                {fancy && <Accordion defaultExpanded>
                    <AccordionPanelSummary
                        aria-controls="filter-options-content"
                        id="filter-options-header"
                    >
                        <div>Saved Filters</div>
                    </AccordionPanelSummary>
                    <AccordionPanelDetails>
                        <div>
                            {datasetFilters.length === 0 &&
                            <Box color="text.secondary" style={{paddingLeft: 10}}>No saved filters</Box>}
                            {datasetFilters.length > 0 && <div><List dense={true}>
                                {datasetFilters.map(item => (
                                    <ListItem key={item.id} data-key={item.id} button
                                              selected={item.id === savedDatasetFilter.id}
                                              onClick={e => this.openDatasetFilter(item.id)}>
                                        <ListItemText primary={item.name}/>
                                        <ListItemSecondaryAction onClick={e => this.deleteDatasetFilter(item.id)}>
                                            <IconButton edge="end" aria-label="delete">
                                                <DeleteIcon/>
                                            </IconButton>
                                        </ListItemSecondaryAction>
                                    </ListItem>
                                ))}
                            </List>
                                <Button onClick={this.props.handleExportDatasetFilters}>Export Filters</Button>
                            </div>}
                        </div>
                    </AccordionPanelDetails>
                </Accordion>}
            </div>
        );
    }
}

const mapStateToProps = state => {
    return {
        dataset: state.dataset,
        markers: state.markers,
        binValues: state.binValues,
        binSummary: state.binSummary,
        numberOfBins: state.numberOfBins,
        embeddingData: state.embeddingData,
        embeddingLabels: state.embeddingLabels,
        interpolator: state.interpolator,
        markerOpacity: state.markerOpacity,
        pointSize: state.pointSize,
        primaryTraceKey: state.primaryTraceKey,
        savedDatasetFilter: state.savedDatasetFilter,
        serverInfo: state.serverInfo,
        embeddings: state.embeddings,
        searchTokens: state.searchTokens,
        unselectedMarkerOpacity: state.unselectedMarkerOpacity,
        combineDatasetFilters: state.combineDatasetFilters,
        datasetFilter: state.datasetFilter,
        datasetFilters: state.datasetFilters,
        selection: state.selection,
        chartSize: state.chartSize
    };
};
const mapDispatchToProps = (dispatch, ownProps) => {
    return {
        handleDialog: (value) => {
            dispatch(setDialog(value));
        },
        handlePrimaryTraceKey: (value) => {
            dispatch(setPrimaryTraceKey(value));
        },
        handleInterpolator: value => {
            dispatch(setInterpolator(value));
        },
        handleChartSize: (value) => {
            dispatch(setChartSize(value));
        },
        handleCombineDatasetFilters: (value) => {
            dispatch(setCombineDatasetFilters(value));
        },
        downloadSelectedIds: () => {
            dispatch(downloadSelectedIds());
        },
        removeDatasetFilter: (filter) => {
            dispatch(removeDatasetFilter(filter));
        },
        handleEmbeddings: value => {
            dispatch(setSelectedEmbedding(value));
        },

        handleNumberOfBins: value => {
            dispatch(setNumberOfBins(value));
        },
        handlePointSize: value => {
            dispatch(setPointSize(value));
        },

        handleMarkerOpacity: value => {
            dispatch(setMarkerOpacity(value));
        },

        handleEmbeddingLabel: value => {
            dispatch(toggleEmbeddingLabel(value));
        },
        handleUnselectedMarkerOpacity: value => {
            dispatch(setUnselectedMarkerOpacity(value));
        },

        handleBinSummary: value => {
            dispatch(setBinSummary(value));
        },
        handleBinValues: value => {
            dispatch(setBinValues(value));
        },
        handleSearchTokens: (value, type) => {
            dispatch(setSearchTokens(value == null ? [] : value, type));
        },
        handleOpenDatasetFilter: value => {
            dispatch(openDatasetFilter(value));
        },
        handleDeleteDatasetFilter: value => {
            dispatch(deleteDatasetFilter(value));
        },
        handleExportDatasetFilters: () => {
            dispatch(exportDatasetFilters());
        },
        handleDeleteFeatureSet: value => {
            dispatch(deleteFeatureSet(value));
        },

    };
};

export default withStyles(styles)(connect(
    mapStateToProps, mapDispatchToProps,
)(SideBar));


