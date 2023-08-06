from .anonymizationOperationInterface import AnonymizationOperationInterface
import collections

# k-means
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
import numpy as np
from kmodes.kmodes import KModes
import numbers
from ppdp_anonops.utils import euclidClusterHelper


class Condensation(AnonymizationOperationInterface):

    def __init__(self):
        super(Condensation, self).__init__()

    def CondenseEventAttributeBykMeanClusterUsingMode(self, xesLog, sensitiveAttribute, descriptiveAttributes, k_clusters):
        allAttributes = descriptiveAttributes.copy()
        allAttributes.append(sensitiveAttribute)

        values = self._getEventMultipleAttributeValues(xesLog, allAttributes)
        values, valueToOneHotDict, oneHotToValueDict = euclidClusterHelper.oneHotEncodeNonNumericAttributes(allAttributes, values)

        kmeans = KMeans(n_clusters=k_clusters)
        kmeans.fit(values)

        # Get a dict with the value as key and the cluster it is assigned to as value
        valueToClusterDict = self.__getValuesOfSensitiveAttributePerClusterAsDict(kmeans.labels_, values)
        clusterModeDict = self.__getModeOfSensitiveAttributePerCluster(kmeans.labels_, values, k_clusters)

        # Apply clustered data mode to log
        for case_index, case in enumerate(xesLog):
            for event_index, event in enumerate(case):
                if(sensitiveAttribute in event.keys()):
                    if sensitiveAttribute in valueToOneHotDict.keys():
                        oneHotOfValue = valueToOneHotDict[sensitiveAttribute][event[sensitiveAttribute]]
                        clusterOfValue = valueToClusterDict[oneHotOfValue]
                        valueOfOneHot = oneHotToValueDict[sensitiveAttribute][clusterModeDict[clusterOfValue]]
                        event[sensitiveAttribute] = valueOfOneHot
                    else:
                        event[sensitiveAttribute] = clusterModeDict[valueToClusterDict[event[sensitiveAttribute]]]

        return self.AddExtension(xesLog, 'con', 'event', sensitiveAttribute)

    def CondenseCaseAttributeBykMeanClusterUsingMode(self, xesLog, sensitiveAttribute, descriptiveAttributes, k_clusters):
        allAttributes = descriptiveAttributes.copy()
        allAttributes.append(sensitiveAttribute)

        values = self._getCaseMultipleAttributeValues(xesLog, allAttributes)
        values, valueToOneHotDict, oneHotToValueDict = euclidClusterHelper.oneHotEncodeNonNumericAttributes(allAttributes, values)

        kmeans = KMeans(n_clusters=k_clusters)
        kmeans.fit(values)

        # Get a dict with the value as key and the cluster it is assigned to as value
        valueToClusterDict = self.__getValuesOfSensitiveAttributePerClusterAsDict(kmeans.labels_, values)
        clusterModeDict = self.__getModeOfSensitiveAttributePerCluster(kmeans.labels_, values, k_clusters)

        # Apply clustered data mode to log
        for case_index, case in enumerate(xesLog):
            if(sensitiveAttribute in case.attributes.keys()):
                if sensitiveAttribute in valueToOneHotDict.keys():
                    oneHotOfValue = valueToOneHotDict[sensitiveAttribute][case.attributes[sensitiveAttribute]]
                    clusterOfValue = valueToClusterDict[oneHotOfValue]
                    valueOfOneHot = oneHotToValueDict[sensitiveAttribute][clusterModeDict[clusterOfValue]]
                    case.attributes[sensitiveAttribute] = valueOfOneHot
                else:
                    case.attributes[sensitiveAttribute] = clusterModeDict[valueToClusterDict[case.attributes[sensitiveAttribute]]]

        return self.AddExtension(xesLog, 'con', 'case', sensitiveAttribute)

    def CondenseEventAttributeBykModesClusterUsingMode(self, xesLog, sensitiveAttribute, descriptiveAttributes, k_clusters):
        # Make sure the sensitive attribute is last in line for later indexing
        allAttributes = descriptiveAttributes.copy()
        allAttributes.append(sensitiveAttribute)

        values = self._getEventMultipleAttributeValues(xesLog, allAttributes)
        km = KModes(n_clusters=k_clusters, init='random')
        clusters = km.fit_predict(values)

        # Get a dict with the value as key and the cluster it is assigned to as value
        valueToClusterDict = self.__getValuesOfSensitiveAttributePerClusterAsDict(clusters, values)
        clusterModeDict = self.__getModeOfSensitiveAttributePerCluster(clusters, values, k_clusters)

        # Apply clustered data mode to log
        for case_index, case in enumerate(xesLog):
            for event_index, event in enumerate(case):
                if(sensitiveAttribute in event.keys()):
                    clusterOfValue = valueToClusterDict[event[sensitiveAttribute]]
                    event[sensitiveAttribute] = clusterModeDict[clusterOfValue]

        return self.AddExtension(xesLog, 'con', 'event', sensitiveAttribute)

    def CondenseCaseAttributeBykModesClusterUsingMode(self, xesLog, sensitiveAttribute, descriptiveAttributes, k_clusters):
        # Make sure the sensitive attribute is last in line for later indexing
        allAttributes = descriptiveAttributes.copy()
        allAttributes.append(sensitiveAttribute)

        values = self._getCaseMultipleAttributeValues(xesLog, allAttributes)
        km = KModes(n_clusters=k_clusters, init='random')
        clusters = km.fit_predict(values)

        # Get a dict with the value as key and the cluster it is assigned to as value
        valueToClusterDict = self.__getValuesOfSensitiveAttributePerClusterAsDict(clusters, values)
        clusterModeDict = self.__getModeOfSensitiveAttributePerCluster(clusters, values, k_clusters)

        # Apply clustered data mode to log
        for case_index, case in enumerate(xesLog):
            if(sensitiveAttribute in case.attributes.keys()):
                clusterOfValue = valueToClusterDict[case.attributes[sensitiveAttribute]]
                case.attributes[sensitiveAttribute] = clusterModeDict[clusterOfValue]

        return self.AddExtension(xesLog, 'con', 'case', sensitiveAttribute)

    def CondenseEventAttributeByEuclidianDistance(self, xesLog, sensitiveAttribute, descriptiveAttributes, weightDict, k_clusters):
        attributes = descriptiveAttributes
        attributes.append(sensitiveAttribute)
        weights = [weightDict[a] for a in attributes]

        values = []
        for case_index, case in enumerate(xesLog):
            for event_index, event in enumerate(case):
                eventValues = []
                for attr in attributes:
                    eventValues.append(event[attr])
                values.append(eventValues)

        cluster = euclidClusterHelper.euclidDistCluster_Fit(values, k_clusters, weights)
        i = 0
        for case_index, case in enumerate(xesLog):
            for event_index, event in enumerate(case):
                event[sensitiveAttribute] = cluster['categories'][cluster['labels'][i]]
                i = i + 1

        return self.AddExtension(xesLog, 'con', 'event', sensitiveAttribute)

    def CondenseCaseAttributeByEuclidianDistance(self, xesLog, sensitiveAttribute, descriptiveAttributes, weightDict, k_clusters):
        # Move Unique-Event-Attributes up to trace attributes
        attributes = descriptiveAttributes
        attributes.append(sensitiveAttribute)
        weights = [weightDict[a] for a in attributes]

        values = []
        for case_index, case in enumerate(xesLog):
            caseValues = []
            for attr in attributes:

                # Check whether the attribute is a unique event attribute (Only occuring once and in the first event)
                if(attr not in case.attributes.keys()):
                    # Ensure the attribute exists, even if it is None
                    val = None

                    unique = True
                    for event_index, event in enumerate(case):
                        if ((event_index == 0 and attr not in event.keys()) or (event_index > 0 and attr in event.keys())):
                            unique = False

                    if(unique):
                        val = case[0][attr]
                    caseValues.append(val)
                else:
                    caseValues.append(case.attributes[attr])
            values.append(caseValues)

        cluster = euclidClusterHelper.euclidDistCluster_Fit(values, k_clusters, weights)
        i = 0
        for case_index, case in enumerate(xesLog):
            case.attributes[sensitiveAttribute] = cluster['categories'][cluster['labels'][i]]
            i = i + 1

        return self.AddExtension(xesLog, 'con', 'case', sensitiveAttribute)

    def __getMode(self, valueList):
        if len(valueList) == 0:
            return 0

        s = {}
        for v in valueList:
            if v in s:
                s[v] += 1
            else:
                s[v] = 1

        # Sort dict by value
        s = {k: v for k, v in sorted(s.items(), key=lambda item: item[1])}
        return next(iter(s.keys()))

    # Make sure all values provided are actually numeric
    def __checkNumericAttributes(self, values):
        numCheck = [x for x in values if not isinstance(x, numbers.Number)]
        if(len(numCheck) > 0):
            raise NotImplementedError("Use a numeric attribute")
        pass

    def __getValuesOfSensitiveAttributePerClusterAsDict(self, clusterLabels, values):
        valueToClusterDict = {}
        for i in range(len(clusterLabels)):
            # [-1] as the sensitive attribute value is always the last in the list
            if values[i][-1] not in valueToClusterDict.keys():
                valueToClusterDict[values[i][-1]] = clusterLabels[i]
        return valueToClusterDict

    def __getModeOfSensitiveAttributePerCluster(self, clusterLabels, values, k_clusters):
        clusterValues = {k: [] for k in range(k_clusters)}
        for i in range(len(clusterLabels)):
            clusterValues[clusterLabels[i]].append(values[i][-1])

        modeDict = {k: 0 for k in range(k_clusters)}
        for k in range(k_clusters):
            modeDict[k] = self.__getMode(clusterValues[k])

        return modeDict
